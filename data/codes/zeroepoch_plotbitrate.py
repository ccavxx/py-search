#!/usr/bin/env python3## FFProbe Bitrate Graph## Copyright (c) 2013, Eric Work# All rights reserved.## Redistribution and use in source and binary forms, with or without# modification, are permitted provided that the following conditions are met:##   Redistributions of source code must retain the above copyright notice, this#   list of conditions and the following disclaimer.##   Redistributions in binary form must reproduce the above copyright notice,#   this list of conditions and the following disclaimer in the documentation#   and/or other materials provided with the distribution.## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE# POSSIBILITY OF SUCH DAMAGE.#
import sys, osimport shutilimport argparseimport subprocess
# prefer C-based ElementTreetry: import xml.etree.cElementTree as etreeexcept ImportError: import xml.etree.ElementTree as etree
# check for matplot libtry: import numpy import matplotlib.pyplot as matplotexcept ImportError:    sys.stderr.write("Error: Missing package 'python3-matplotlib'\n")    sys.exit(1)
# check for ffprobe in pathif not shutil.which("ffprobe"):    sys.stderr.write("Error: Missing ffprobe from package 'ffmpeg'\n")    sys.exit(1)
# get list of supported matplotlib formatsformat_list = list(    matplot.figure().canvas.get_supported_filetypes().keys())matplot.close()  # destroy test figure
# parse command line argumentsparser = argparse.ArgumentParser( description="Graph bitrate for audio/video stream")parser.add_argument('input', help="input file", metavar="INPUT")parser.add_argument('-s', '--stream', help="stream type", choices=["audio", "video"], default="video")parser.add_argument('-o', '--output', help="output file")parser.add_argument('-f', '--format', help="output file format", choices=format_list)args = parser.parse_args()
# check if format given w/o output fileif args.format and not args.output:    sys.stderr.write("Error: Output format requires output file\n")    sys.exit(1)
bitrate_data = {}frame_count = 0frame_rate = None
# get frame data for the selected streamwith subprocess.Popen(    ["ffprobe", "-show_entries", "frame", "-select_streams", args.stream[0], "-print_format", "xml",        args.input    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
 # process xml elements as they close for event in etree.iterparse(proc.stdout):
 # skip non-frame elements        node = event[1] if node.tag != 'frame': continue
 # count number of frames        frame_count += 1
 # get type of frame if args.stream == 'audio':            frame_type = 'A' # pseudo frame type else:            frame_type = node.get('pict_type')
 # get frame rate only once if frame_rate is None:
 # audio frame rate, 1 / frame duration if args.stream == 'audio':                frame_rate = 1.0 / float(node.get('pkt_duration_time'))
 # video frame rate, read stream header else: with subprocess.Popen(                    ["ffprobe", "-show_entries", "stream", "-select_streams", "v", "-print_format", "xml",                        args.input                    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
 # parse stream header xml                    stream_data = etree.parse(proc.stdout)                    stream_elem = stream_data.find('.//stream')
 # compute frame rate from ratio                    frame_rate_ratio = stream_elem.get('avg_frame_rate')                    (dividend, divisor) = frame_rate_ratio.split('/')                    frame_rate = float(dividend) / float(divisor)
 # # frame time (x-axis): # #   ffprobe conveniently reports the frame time position. # # frame bitrate (y-axis): # #   ffprobe reports the frame size in bytes. This must first be #   converted to kbits which everyone is use to. To get instantaneous #   frame bitrate we must consider the frame duration. # #   bitrate = (kbits / frame) * (frame / sec) = (kbits / sec) #
 # collect frame data        frame_time = float(node.get('pkt_pts_time'))        frame_bitrate = (float(node.get('pkt_size')) * 8 / 1000) * frame_rate        frame = (frame_time, frame_bitrate)
 # create new frame list if new type if frame_type not in bitrate_data:            bitrate_data[frame_type] = []
 # append frame to list by type        bitrate_data[frame_type].append(frame)
 # check if ffprobe was successful if frame_count == 0:        sys.stderr.write("Error: No frame data, failed to execute ffprobe\n")        sys.exit(1)
# end frame subprocess
# setup new figurematplot.figure().canvas.set_window_title(args.input)matplot.title("Stream Bitrate vs Time")matplot.xlabel("Time (sec)")matplot.ylabel("Frame Bitrate (kbit/s)")matplot.grid(True)
# map frame type to colorframe_type_color = { # audio 'A': 'red', # video 'I': 'red', 'P': 'green', 'B': 'blue'}
global_peak_bitrate = 0.0global_mean_bitrate = 0.0
# render charts in order of expected decreasing sizefor frame_type in ['I', 'P', 'B', 'A']:
 # skip frame type if missing if frame_type not in bitrate_data: continue
 # convert list of tuples to numpy 2d array    frame_list = bitrate_data[frame_type]    frame_array = numpy.array(frame_list)
 # update global peak bitrate    peak_bitrate = frame_array.max(0)[1] if peak_bitrate > global_peak_bitrate:        global_peak_bitrate = peak_bitrate
 # update global mean bitrate (using piecewise mean)    mean_bitrate = frame_array.mean(0)[1]    global_mean_bitrate += mean_bitrate * (len(frame_list) / frame_count)
 # plot chart using gnuplot-like impulses    matplot.vlines(        frame_array[:,0], [0], frame_array[:,1], color=frame_type_color[frame_type], label="{} Frames".format(frame_type))
# calculate peak line position (left 15%, above line)peak_text_x = matplot.xlim()[1] * 0.15peak_text_y = global_peak_bitrate + (matplot.ylim()[1] * 0.015)peak_text = "peak ({:.0f})".format(global_peak_bitrate)
# draw peak as think black line w/ textmatplot.axhline(global_peak_bitrate, linewidth=2, color='black')matplot.text(peak_text_x, peak_text_y, peak_text, horizontalalignment='center', fontweight='bold', color='black')
# calculate mean line position (right 85%, above line)mean_text_x = matplot.xlim()[1] * 0.85mean_text_y = global_mean_bitrate + (matplot.ylim()[1] * 0.015)mean_text = "mean ({:.0f})".format(global_mean_bitrate)
# draw mean as think black line w/ textmatplot.axhline(global_mean_bitrate, linewidth=2, color='black')matplot.text(mean_text_x, mean_text_y, mean_text, horizontalalignment='center', fontweight='bold', color='black')
matplot.legend()
# render graph to file (if requested) or screenif args.output:    matplot.savefig(args.output, format=args.format)else:    matplot.show()
# vim: ai et ts=4 sts=4 sw=4
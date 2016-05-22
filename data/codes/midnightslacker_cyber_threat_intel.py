#!/usr/bin/env pythonimport urllib2import reimport osimport sysimport shutil
#IPsfile_path = os.environ['HOME']+"/dev/threat_sources/"output_file = os.environ['HOME']+"/lookups/threats.csv"output_dir = os.environ['HOME']+"/lookups"
#Domainsdomain_path = os.environ['HOME']+"/dev/threat_domains/"domain_output = os.environ['HOME']+"/lookups/threat_domains.csv"
#AlienVaultalien = "https://reputation.alienvault.com/reputation.generic"
#Abuse.chzeus = "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist"palevo = "https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist"feodo = "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist"
#Emerging Threatsethreat_blockedIP = "http://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt"ethreat_compromisedIP = "http://rules.emergingthreats.net/blockrules/compromised-ips.txt"ethreat_RBN_malvertisers = "http://doc.emergingthreats.net/pub/Main/RussianBusinessNetwork/emerging-rbn-malvertisers.txt"ethreat_RBN_IP = "http://doc.emergingthreats.net/pub/Main/RussianBusinessNetwork/RussianBusinessNetworkIPs.txt"
#Malc0de Black Listmalcode = "http://malc0de.com/bl/IP_Blacklist.txt"
#Malware Domain List - list of active ip addressesmalwareDom = "http://www.malwaredomainlist.com/hostslist/ip.txt"
#OpenBL.orgopenBL = "http://www.openbl.org/lists/base.txt"
#NoThink.org -- DNS, HTTP and IRCntDNS = "http://www.nothink.org/blacklist/blacklist_malware_dns.txt"ntHTTP = "http://www.nothink.org/blacklist/blacklist_malware_http.txt"ntIRC = "http://www.nothink.org/blacklist/blacklist_malware_irc.txt"
#Blocklist.deblockList = "http://www.blocklist.de/lists/all.txt"
#Dragon Research GroupDRG_vncProbe = "https://www.dragonresearchgroup.org/insight/vncprobe.txt"DRG_http = "https://www.dragonresearchgroup.org/insight/http-report.txt"DRG_ssh = "https://www.dragonresearchgroup.org/insight/sshpwauth.txt"
#Project Honey Pothoney_pot = "http://www.projecthoneypot.org/list_of_ips.php?rss=1"
#CI Armyci_army = "http://www.ciarmy.com/list/ci-badguys.txt"
#danger.rules.skdanger_rules = "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
#SANSsans_ip = "https://isc.sans.edu/ipsascii.html"
#packetmail.netpacket_mail_ip = "https://www.packetmail.net/iprep.txt"
#autoshun.orgautoshun = "http://www.autoshun.org/files/shunlist.csv"
#charles.the-haleys.org -- SSH dictionary attackssh_dict_attack = "http://charles.the-haleys.org/ssh_dico_attack_hdeny_format.php/hostsdeny.txt"
#virbl.orgvirbl_dns_blacklist = "http://virbl.org/download/virbl.dnsbl.bit.nl.txt"
#TOR  nodestor_exit_nodes = "https://check.torproject.org/exit-addresses"
#osint.bambenekconuslting.comosint_iplist = "http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt"
#TALOS IP Blacklisttalos_blacklist = "http://talosintel.com/files/additional_resources/ips_blacklist/ip-filter.blf"
open_source_threat_intel = { "AlienVault_blacklist":alien, "malc0de_blacklist":malcode,  "palevo_ip_blacklist":palevo,   "zeus_tracker_ip_blacklist":zeus, "feodo_black_list":feodo, "emerging_threats_ip_blacklist":ethreat_blockedIP, "emerging_threats_compromised_ips":ethreat_compromisedIP, "emerging_threats_malvertisers":ethreat_RBN_malvertisers, "emerging_threats_RBN_ips":ethreat_RBN_IP, "malware_domain_list_ips":malwareDom, "open_blacklist":openBL, "noThink_DNS_blacklist":ntDNS, "noThink_HTTP_blacklist":ntHTTP, "noThink_IRC_blacklist":ntIRC, "fail2ban":blockList, "DRG_vncProbe":DRG_vncProbe, "DRG_http":DRG_http, "DRG_ssh":DRG_ssh, "project_honey_pot":honey_pot, "ci_army":ci_army, "danger_rules":danger_rules, "isc_SANS":sans_ip, "packet_mail":packet_mail_ip, "autoshun":autoshun, "ssh_bruteforce":ssh_dict_attack, "virbl_dns_blacklist":virbl_dns_blacklist, "tor_exit_nodes":tor_exit_nodes, "osint_iplist":osint_iplist, "talos_blacklist":talos_blacklist    }
# Regular expression for IPv4 Addressesip = re.compile('((?:(?:[12]\d?\d?|[1-9]\d|[1-9])\.){3}(?:[12]\d?\d?|[\d+]{1,2}))')
def regex(threat_list, pattern): ''' Filter pattern from threat_list '''    threat_intel = re.findall(pattern, str(threat_list)) return '\n'.join(threat_intel)
def urlgrab2 (host, pattern): ''' Grab threat intel from host '''    req = urllib2.Request(host) try:        response = urllib2.urlopen(host) except urllib2.URLError as e: if hasattr(e, 'reason'): print "\t [-] Failed to reach " + str(host) +"\n\t [-] Reason: ", str(e.reason) +"\n"            sys.exit() elif hasattr(e, 'code'): print "\t [-] The server (%s) couldn't fulfill the requst.\n\t [-] Reason: %s" % (host, e.code)            sys.exit()     threat_list = response.readlines() return regex(threat_list, pattern)

def writeToFile (source_path, threat_list, filename): ''' Write updated threat intel to correct file and directory ''' # check if file already exists, if it does, overwrite it. If the file doesn't exist, create it. if os.path.isfile(source_path+filename):        f = open(source_path+filename, 'r+')        f.writelines(threat_list)        f.truncate()        f.close() else:        f = open(source_path+filename, 'w+')        f.writelines(threat_list)        f.close()
def createCSV(source_path, directory, oFile, header): ''' Create a two column csv file with threat and source for the columns ''' # Make sure the directory is mounted if not os.path.isdir(directory): print "\t [-] Output directory does not exist or is not mounted\n"        sys.exit()
 # copy old file for diff--then remove to create new file if os.path.isfile(oFile):        shutil.copyfile(oFile, oFile+".old")        os.remove(oFile)  # create header for first line    f = open(oFile, 'w+')    f.write(header)  for hFile in os.listdir(source_path): with open(source_path+hFile) as infile: for line in infile:                f.write(line.rstrip()+","+hFile+"\n")    f.close()
def main(): # Loop through open source threat intelligence sources # Pull them down from the interwebs and format them # Write them to file. for filename, source in open_source_threat_intel.iteritems(): print "[+] Grabbing: " + source        threat_list=urlgrab2(source, ip)        writeToFile(file_path, threat_list, filename)
 # Create CSV print "[+] Creating CSV. . .\n"    createCSV(file_path, output_dir, output_file, "IP,Threat_Feed\n")
 # Now lets create a domain blacklist -- sources are handled by bash script    createCSV(domain_path, output_dir, domain_output, "Domain, Threat_Feed\n")
if __name__ == "__main__":    main()

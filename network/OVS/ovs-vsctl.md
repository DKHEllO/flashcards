# ovs-vsctl

## NAME

**ovs-vsctl** - 查询和配置**ovs-vswithed**的实用工具

## OPTS

**ovs-vsctl**  [**options**]  -- [**options**] **command** [**args**] [-- [**options**] **command** [**args**]]...

## DESCRIPTION

**ovs-vsctl**通过**ovs-vswitched**配置数据库提供的高级别的接口来配置**ovs-vswitchd**。**ovs-vsctl**连接到**ovsdb-server**进程，这个进程包含一个OpenvSwitch配置数据库。通过这个连接**ovs-vsctl**可以根据提供的命令查询和修改这个数据库。如果之后**ovs-vsctl**应用了一些变更，默情况下它会等待直到**ovs-vswitchd**完成重新配置后才退出。（如果想在ovs-vswitchd未运行的情况下使用ovs-vsctl，使用--no-wait参数）

ovs-vsctl可以在一次运行中执行任意数量的命令，作为针对数据库的单个原子事务实现。

### Linux VLAN Bridging Compatibility

ovs-vsctl支持由Open vSwitch实现的网桥模型，其中单个网桥支持多个不同VLan的端。在这个模型中，桥上的每个端口要么是一个trunk口，它可能传递标记了802.1Q标头的包，这些包被标记为VLANs，要么被分配一个从未标记过802.1Q标头的隐式VLAN。

为了与为Linux网桥设计的软件兼容，ovs−vsctl还支持一种模型，在这种模型中，与给定802.1Q VLAN相关的流量被隔离到一个单独的网桥中。add-br命令的一种特殊形式(见下文)在一个OpenvSwitch桥中创建一个“假桥”来模拟这种行为。当这样的“假桥”处于活动状态时，ovs-vsctl将把它看作与其“父桥”分离的桥，但是Open vSwitch中的实际实现只使用一个桥，而假桥上的端口被分配给它们所属的假桥的隐含VLAN。(VLAN0的假网桥接收没有802.1Q标记或VLAN 0标记的包。)

## OPTIONS

−−db=server:配置ovs-vsctl可查询和修改配置的数据库server。server需要使用**ovsdb**中描述的OVSDB主动或被动连接方法。默认使用**unix:/var/run/openvswitch/db.sock**

−−no−wait:阻止ovs−vsctl等待ovs−vswitchd根据修改后的数据库重新配置自身。这个参数应该用在ovs-vswitchd未运行的情况下；否则ovs-vsctl将不会退出直到ovs-vswitchd启动。

−−no−syslog:这个可选项相当于−−verbose=vsctl:syslog:warn

−−oneline：修改输出格式，以便将每个命令的输出打印在单行上。换行符将以\n的形式打印出来，否则在输出中出现的任何\实例都将加倍。为每个没有输出的命令打印空行。此选项不影响列表或查找命令的输出格式;请参阅下面的表格格式选项。

−t secs

−−timeout=secs：默认情况下，或者秒数为0时，ovs−vsctl将永远等待数据库的响应。此选项将运行时间限制为secs秒。如果timeout超时，ovs−vsctl将使用SIGALRM信号退出。(超时通常只在无法联系数据库或系统过载时才会发生。)

#### Public Key Infrastructure Options

−p privkey.pem 

−−private−key=privkey.pem：

指定一个PEM文件，其中包含作为ovs - vsctl的对外SSL连接标识的私有密钥。

−c cert.pem 

−−certificate=cert.pem：

指定一个包含证书的PEM文件，该证书证明在- p或- private - key上指定的私钥是可信的。证书必须由证书颁发机构(CA)签名，SSL连接中的对等方将使用CA对其进行验证。

−C cacert.pem 

−−ca−cert=cacert.pem：

指定一个包含CA证书的PEM文件，ovs−vsctl应该使用该文件来验证SSL对等方提供给它的证书。(这可以是SSL对等点用来验证−c或−证书上指定的证书的同一证书，也可以是不同的证书，具体取决于使用的PKI设计。)

−C none 

−−ca−cert=none：

禁用SSL对等点提供的证书验证。这就引入了安全风险，因为这意味着无法验证证书是否是已知可信主机的证书。

−−bootstrap−ca−cert=cacert.pem：

当cacert.pem存在时这个选项与与- C或- ca - cert的效果相同。如果它不存在，那么ovs - vsctl将尝试在其第一个SSL连接上从SSL对等端获取CA证书，并将其保存到指定的PEM文件。如果成功，它将立即删除连接并重新连接，从那时起，所有SSL连接都必须通过由获得的CA证书签名的证书进行身份验证。**此选项将SSL连接暴露给获得初始CA证书的中间人攻击**，但它可能对引导非常有用。 

只有当SSL对等方将其CA证书作为SSL证书链的一部分发送时，此选项才有用。SSL协议不要求服务器发送CA证书。

这个选项与−C和−ca−cert是相互排斥的。

−−peer−ca−cert=peer-cacert.pem：

指定包含要发送给SSL对等点的一个或多个附加证书的PEM文件。peercacert.pem应该是CA证书，用于签署ovs- vsctl自己的证书，即−c或−certificate上指定的证书。如果ovs-vsctl的证书是自签名的，则-certificate和-peer-ca- cert应指定相同的文件。
此选项在正常操作中没有用处，因为SSL对等方必须已经拥有CA证书，以便对等方对ovs-vsctl的身份有任何信心。然而，这为新安装提供了一种方法，在它的第一个SSL连接上引导CA证书。

−−log−file[=file]：默认是/var/log/openvswitch/ovs−vsctl.log

−−syslog−target=host:port

## COMMANDS

### Open vSwitch Commands

init：

初始化OpenvSwitch数据库(如果它是空的)。如果数据库已经初始化，则此命令无效。
如果OpenvSwitch数据库为空，任何成功的ovs-vsctl命令都会自动初始化该数据库。提供此命令是为了初始化数据库，而不执行任何其他命令。

show:

打印数据库内容的简要概述。

emer−reset:

将配置重置为clean状态。它取消OpenFlow控制器、OVSDB服务器和SSL，并删除端口镜像、故障模式、NetFlow、sFlow和IPFIX配置。该命令还从所有数据库记录中删除other-config键，但如果other-config:hwaddr存在于网桥记录中，则保留other-config:hwaddr。其他网络配置保持原样。

#### Bridge Commands

[−−may−exist] add−br bridge：

创建一个叫bridge的网桥。最初，这个网桥没有端口。

[−−may−exist] add−br bridge parent vlan：

在现有的Open vSwitch网桥parent节点中创建一个名为bridge的“假网桥”，该网桥必须已经存在，并且本身不能是一个假网桥。新的假桥将在802.1Q VLAN vlan上，vlan必须是0到4095之间的整数。父网桥必须没有用于该vlan的假网桥。最初bridge将没有端口(除了桥本身)。

[−−if−exists] del−br bridge：

删除bridge和它下面的所有接口。如果bridge是一个真实的网桥，这个命令也会删除任何以bridge为父节点的所有假网桥包括所有端口

[−−real|−−fake] list−br：

通过标准的输出列出所有存在的实体网桥和虚拟网桥，一个网桥一行。

br−exists bridge

br−to−vlan bridge

br−to−parent bridge

br−set−external−id bridge key [value]

#### Port Commands

list−ports bridge:

列出网桥的所有端口

[−−may−exist] add−port bridge port [column[:key]=value]...：

可选参数设置命令创建的端口记录中的column值。例如，tag=9将使该端口成为VLAN 9的访问端口。其语法与set命令相同(参见下面的数据库命令)。

[−−if−exists] del−port [bridge] port：

[−−if−exists] −−with−iface del−port [bridge] iface：

Deletes the port named iface or that has an interface named iface

port−to−br port：

#### Bond Commands

这些命令运行在具有多个接口的端口，这个端口OpenvSwitch通过“bonds”调用。

[−−fake−iface] add−bond bridge port iface... [column[:key]=value]...：

添加bond口

在bridge上创建一个名为port的新端口，它将每个iface的网络设备连接在一起。必须至少命名两个接口。如果接口启用了DPDK，那么事务将需要包括显式设置接口类型为' DPDK '的操作。
可选参数设置命令创建的端口记录中的列值。其语法与set命令相同(参见下面的数据库命令)。

[−−may−exist] add−bond−iface bond iface:

添加bond成员口

[−−if−exists] del−bond−iface [bond] iface:

删除bond成员口。如果删除iface导致其bond口只有一个接口，则该端口将从一个bond口转换为一个普通端口。如果iface是bond口中唯一的接口，则为错误。

#### Interface Commands

These commands examine the interfaces attached to an Open vSwitch bridge

list−ifaces bridge

iface−to−br iface

#### OpenFlow Controller Connectivity

ovs−vswitchd可以在本地执行所有桥接和交换的配置，也可以配置为与一个或多个外部OpenFlow控制器通信。交换机通常配置为连接到主控制器，主控制器负责网桥的流表，以实现网络策略。此外，可以将交换机配置为侦听来自服务控制器的连接。服务控制器通常用于偶尔的支持和维护，例如使用ovs−ofctl。

get−controller <u>*bridge*</u>

del−controller *<u>bridge</u>*

set−controller *<u>bridge</u>* <u>*target*</u>...

设置已配置的控制器。每个<u>*target*</u>可使用下列任何一种形式:

- ssl:host[:port]

- tcp:host[:port]

  The specified port on the given host, which can be expressed either as a DNS name (if built with unbound library) or an IP address in IPv4 or IPv6 address format. Wrap IPv6 addresses in square brackets, e.g. tcp:[::1]:6653.

- unix:file

  On POSIX, a Unix domain server socket named file.

- pssl:\[port\]\[:host]

- ptcp:\[port][:host]

- punix:file

<u>*Controller Failure Settings*</u>

在配置控制器时，它通常负责配置交换机上的所有流表。因此，如果到控制器的连接失败，网络就不能建立新的连接。如果到控制器的连接断掉的时间足够长，则根本没有任何数据包可以通过交换机。

如果该值是**standalone**，或者没有设置这些设置，那么在三次于不活动探测间隔的时间内，当没有从控制器接收到任何消息时，ovs−vswitchd将接管配置流表的任务。在这种模式下，ovs−vswitchd使数据路径像普通的MAC-learning交换机一样工作。ovs−vswitchd将继续在后台重试连接控制器，当连接成功时，它将停止其独立行为。

如果将此选项设置为secure，则当控制器连接失败时，ovs−vswitchd将不会自己配置流流表。

get−fail−mode <u>*bridge*</u>

del−fail−mode <u>*bridge*</u>

set−fail−mode <u>*bridge*</u> **standalone**|**secure**

## EXAMPLES

Set the qos column of the Port record for eth0 to point to a new QoS record, which in turn points with its queue 0 to a new Queue record: 

ovs−vsctl −− set port eth0 qos=@newqos −− −−id=@newqos create qos type=linux−htb other−config:max−rate=1000000 queues:0=@newqueue −− −−id=@newqueue create queue other−config:min−rate=1000000 other−config:max−rate=1000000

## CONFIGURATION COOKBOOK

**Port Configuration** 

Add an ‘‘internal port’’ vlan10 to bridge br0 as a VLAN access port for VLAN 10, and configure it with an IP address: 

ovs−vsctl add−port br0 vlan10 tag=10 −− set Interface vlan10 type=internal ip addr add 192.168.0.123/24 dev vlan10 

Add a GRE tunnel port gre0 to remote IP address 1.2.3.4 to bridge br0: 

ovs−vsctl add−port br0 gre0 −− set Interface gre0 type=gre options:remote_ip=1.2.3.4

**Port Mirroring**

Mirror all packets received or sent on eth0 or eth1 onto eth2, assuming that all of those ports exist on bridge br0 (as a side-effect this causes any packets received on eth2 to be ignored):

ovs−vsctl −− set Bridge br0 mirrors=@m \

−− −−id=@eth0 get Port eth0 \ 

−− −−id=@eth1 get Port eth1 \ 

−− −−id=@eth2 get Port eth2 \ 

−− −−id=@m create Mirror name=mymirror select-dst-port=@eth0,@eth1 select-srcport=@eth0,@eth1 output-port=@eth2 

Remove the mirror created above from br0, which also destroys the Mirror record (since it is now unreferenced): 

ovs−vsctl −− −−id=@rec get Mirror mymirror \ 

−− remove Bridge br0 mirrors @rec 

The following simpler command also works: 

ovs−vsctl clear Bridge br0 mirrors
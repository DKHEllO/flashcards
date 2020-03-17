# ovn-architecture

## DESCRIPTION

开放虚拟网络OVN是一个支持虚拟网络抽象层的系统。OVN补充了OVS的现有功能，以添加对虚拟网络抽象层的原生支持，如`虚拟L2`和`L3 overlays`和`安全组`。与OVS一样，OVN的设计目标是拥有一个可大规模运行的高质量的生产级实现。

OVN部署环境包含以下几个组件:

- `Cloud Management System (CMS)`，这是OVN的最终客户端(通过它的用户和管理员)。OVN集成需要安装一个cms特定的插件和相关软件(参见下面)。OVN最初将`OpenStack`作为CMS的目标。

  我们通常提到“CMS”，但是可以想象多个CMS管理OVN部署的不同部分的场景。

- 安装在中心位置的OVN数据库物理或虚拟节点(最终是集群)。

- 一个或多个(通常是多个)管理程序(hypervisor)，管理程序必须运行`Open vSwitch`并实现OVS源代码中的描述的`IntegrationGuide.rst`接口。任何由Open vSwitch支持的管理程序平台都是可以接受的。

- 0个或多个网关。网关通过双向转发报文的隧道和物理以太网端口，将基于隧道的逻辑网络扩展到物理网络。这允许非虚拟化的机器参与逻辑网络。网关可以是物理主机、虚拟机或支持**vtep(5)**标准的基于asic的硬件交换机。

  管理程序和网关一起称为传输节点或chassis。

下图显示了OVN的主要组件和相关软件是如何交互的，从图的顶部开始：

- CMS

- OVN/CMS插件是CMS相对于OVN的接口。在OpenStack中这是Neutron插件。这个插件的主要目的是翻译CMS的逻辑网络配置意图，并转换为OVN可以理解的中间表示形式并按照CMS指定的格式将它存储在CMS配置数据库中。

  这个组件CMS指定的必须组件，因此需要为每个与OVN集成的CMS开发新的插件。图中这个组件下面的所有组件都是与cms无关的。

- OVN向北数据库接收OVN/CMS插件传递的逻辑网络配置的中间态表示形式。数据库schema意味着CMS中使用的概念`impedance` `match`（未想好怎么翻译。。。），因此，它直接支持逻辑交换机、路由器、acl等概念。详见**ovn−nb(5)**。

  OVN向北数据库只有两个`client`:上面的OVN/CMS插件和下面的`OVN - northd`插件。

- `ovn−northd(8)`连接上面提到的OVN北向数据库和下面所说的OVN南向数据库。它依照传统的网络的概念将OVN北向数据库中的逻辑网络配置翻译成了下面OVN南向数据库中的逻辑`datapath flows`（流表？）

- OVN南行数据库是整个系统的核心。它的客户端是上面所提到的`ovn-northd(8)`和下面提到的每个传输节点的`ovn-controller`。

  OVN南行数据库包含以下三种数据:

  - 指定如何访问`hypervisor`和其他节点的物理网络(PN)表
  - 依照`logical datapath flows`描述逻辑网络的逻辑网络(LN)表
  - 将逻辑网络组件(components’ locations)链接到物理网络的`Binding`表

​       `hypervisors`填充`PN`和`Port_Binding`表，而`ovn−northd`(8)填充`LN`表。

​       OVN南向数据库的表现随着传输节点的数量而变化。当我们遇到瓶颈时，这可能需要在`ovsdb - server(1)`		上做 一些工作。可能需要集群以获取可用性。

其余组件被复制到每个`hypervisor`上:

- **ovn−controller(8)**是ovn在每个hypervisor和software gateway上的代理。Northbound，它连接了OVN的南向数据库，以了解OVN配置和状态，并通过hypervisor的状态去填充PN表和Binding表的Chassis列，Southbound，它作为一个OpenFlow controller连接到**ovs-vswitchd(8)**，控制网络流量，并连接到本地ovsdb−server(1)，以允许它监视和控制OpenvSwitch的配置。
- **ovs−vswitchd(8)**和**ovsdb−server(1)**是Open vSwitch的常规组件。

![image-20200307180315308](https://github.com/DKHEllO/flashcards/blob/develop/image/image-20200307180315308.png)

**Information Flow in OVN**

OVN中的配置数据从北向南流动。CMS通过其OVN/CMS插件，将逻辑网络配置通过northbound数据库传递给OVN - northd。然后，ovn−northd将配置编译为较低级别的形式，并通过南向数据库将其传递给所有的设备。

OVN中的状态信息从南向北流动。OVN目前只提供几种形式的状态信息。首先，**ovn−northd**填充向北行的**Logical_Switch_Port**表中的**up**列：如果南向**Port_Binding**表中的逻辑端口的**chassis**列不为空，则将其设置为**true**，否则设置为**false**。这允许CMS检测VM的网络何时联通。

其次，OVN向CMS反馈配置生效的情况，即CMS提供的配置是否生效。此功能要求CMS参与一个（sequence number）协议，其工作方式如下：

- 当CMS更新北行数据库中的配置时，与此同时，它将增加NB_Global表中的nb_cfg列的值（只有当CMS想知道配置何时生效时，才需要这样做。）
- 当ovn−northd基于向北数据库的给定快照更新向南数据库时，与此同时，它将nb_cfg从向北的NB_Global复制到向南的数据库SB_Global表中（因此，监视两个数据库的进程可以确定南向数据库的配置何时与北向数据库同步。）
- ovn−northd收到来自南行数据库服务器的确认，确认其更改已提交后，将北行NB_Global表中的sb_cfg更新为下推的nb_cfg版本。（因此，CMS或其他进程可以在没有连接到南向数据库的情况下确定南向数据库的配置何时同步。）
- 每个设备上的ovn−controller进程接收到更新了nb_cfg的南向数据库。这个进程反过来更新本地的的Open vSwitch实例中的流表。当它从Open vSwitch接收到流表已被更新的确认时，它将更新南向数据库中自己的Chassis记录中的nb_cfg。
- ovn−northd监视southbound数据库中所有Chassis记录中的nb_cfg列。它跟踪所有记录中的最小值，并将其复制到向北行的NB_Global表的hv_cfg列中。（因此，CMS或其它进程可以确定所有的hypervisor何时完成了北向的配置）


# OVS安装

## 一、Obtaining Open vSwitch Sources

获取源码

```
$ git clone https://github.com/openvswitch/ovs.git
```

默认会使用master分支，如果你想构建一个特殊版本，可以`checkout`到一个指定的分支进行编译：

```
$ git checkout v2.7.0
```

该仓库里每个发布版本都有一个分支，例如，在Open vSwitch 2.7.x发布分支中包含最新的更改，这里面可能包括尚未发布版本的bug修复，你可以通过ovs目录切换到这个分支：

```
$ git checkout origin/branch-2.7
```

## 二、Build Requirements

需要编译Open vSwitch发行版中的用户态程序，需要以下依赖:

- GNU make
- A C compiler, such as:

  - GCC 4.6 or later.
  - Clang 3.4 or later.
  - MSVC 2013. Refer to [Open vSwitch on Windows](http://docs.openvswitch.org/en/latest/intro/install/windows/) for additional Windows build instructions.
  虽然OVS可能与其他编译器兼容，但是可能缺少对原子操作的最佳支持，这使得OVS非常慢(请参阅lib/ OVS -  atom .h)
- libssl, from OpenSSL，该库是可选的但是推荐安装。如果你计划将OVS连接到OpenFlow控制器，则推荐使用。需要libssl保证OVS到OpenFlow控制器的连接的机密性和真实性。如果安装了libssl，那么Open vSwitch将自动构建并支持它。
- libcap-ng，该库是可选的但是推荐安装。它可以让非root用户不需要以root用户权限来运行OVS守护进程。如果安装了libcap-ng，那么Open vSwitch将自动构建并支持它。
- Python 3.4 or later.
- Unbound library, from [http://www.unbound.net](http://www.unbound.net/),是可选的，但如果希望启用ovs-vswitchd和其他实用程序在指定OpenFlow和OVSDB远端时使用DNS解析时建议使用，如果已经安装了unbound库，那么Open vSwitch将自动构建并支持它。环境变量OVS_RESOLV_CONF可用于指定DNS服务器配置文件（默认配置文件在/etc/resolv.conf）

在Linux上，您可以选择编译Open vSwitch发行版附带的内核模块，或者使用内置于Linux内核中的内核模块(version 3.3 or later)。请参阅 [Open vSwitch FAQ](http://docs.openvswitch.org/en/latest/faq/) “作为上游Linux内核的一部分发布的Open vSwitch内核datapath中哪些特性不可用?”，你也可以只使用用户态实现，但要在feature和性能上付出一些代价，更多细节参考 [Open vSwitch without Kernel Support](http://docs.openvswitch.org/en/latest/intro/install/userspace/)。

要编译Linux上的内核模块，还必须安装以下依赖：

- A supported Linux kernel version

  对于可选的ingress policeing，你必须启用内核配置选项NET_CLS_BASIC、NET_SCH_INGRESS和NET_ACT_POLICE(内置或作为模块)， `NET_CLS_POLICE`已经过时了不需要了。

  在3.11之前的内核中，对于IP GRE隧道(NET_IPGRE)， ip_gre模块不能被加载或编译。

  要使用Open vSwitch配置HTB或HFSC服务质量，您必须启用相应的配置选项。

  要使用Open vSwitch对TAP设备的支持，您必须启用CONFIG_TUN。

- 要构建内核模块，需要使用与构建内核相同的GCC版本
- 与模块要运行的Linux内核映像对应的内核构建目录。例如，在Debian和Ubuntu下，每个包含内核二进制文件的linux-image包都有一个对应的linux-headers包，该包具有所需的构建基础结构。

如果您使用的是Git或snapshot(而不是发布包)，或者修改了Open vSwitch构建系统或数据库schema，那么您还需要以下依赖：

- Autoconf version 2.63 or later.
- Automake version 1.10 or later.
- libtool version 2.4 or later. (Older versions might work too.)

用户空间datapath测试和Linux datapath也依赖于:

- pyftpdlib. Version 1.2.0 is known to work. Earlier versions should also work.
- GNU wget. Version 1.16 is known to work. Earlier versions should also work.
- netcat. Several common implementations are known to work.
- curl. Version 7.47.0 is known to work. Earlier versions should also work.
- tftpy. Version 0.6.2 is known to work. Earlier versions should also work.
- netstat. Available from various distro specific packages

db(5)手册页将包括一个E-R关系图，除纯文字外的其他格式，只适用于下列情况:

- dot from graphviz (http://www.graphviz.org/).

如果您打算大量修改Open vSwitch，请考虑安装以下软件在编译过程中获得更全面的Warning:

- “sparse” version 0.5.1 or later (https://git.kernel.org/pub/scm/devel/sparse/sparse.git/).
- GNU make.
- clang, version 3.4 or later
- flake8 along with the hacking flake8 plugin (for Python code). 针对Python代码运行的自动flake8检查启用了一些来自“hacking”flake8插件的警告。如果没有安装，警告将不会出现，直到它在安装了“hacking”的系统上运行。

您可能会发现在**utilities**/ovs-dev.py中找到的ovs-dev脚本，它非常有用。

## 三、Installation Requirements

构建Open vSwitch的机器可能并不运行它。要简单地安装和运行Open vSwitch，您需要以下软件:

- 与构建使用的共享库兼容。
- 在Linux上，如果您想使用基于内核的datapath，那么应该使用具有兼容内核模块的内核。这可以是使用Open vSwitch构建的内核模块(例如，在前面的步骤中)，也可以是Linux 3.3或更高版本附带的内核模块。Open vSwitch的特性和性能可以根据模块和内核的不同而有所不同，更多参考[Releases](http://docs.openvswitch.org/en/latest/faq/releases/) 
- 对于可选的的ingress policing，来自iproute2的“tc”程序(它是所有主要发行版的一部分，可以从https://wiki.linuxfound.org/networking/iproute2获得)。
- Python 3.4 or later.

在Linux上，您应该确保/dev/urandom存在。为了支持TAP设备，您还必须确保/dev/net/tun存在。

## 四、Bootstrapping

如果下载了已发布的tarball，则不需要执行此步骤.如果您直接从OVS 仓库获取的代码或者快照，那么在顶部的源代码目录中运行`boot.sh`来构建`configure`脚本：

```
$ ./boot.sh`
```

## 五、Configuring

通过运行Configure脚本来配置包。通常可以不带任何参数地调用configure。例如:

```
$ ./configure
```

默认情况下，所有文件都安装在/usr/local下。Open vSwitch还希望在/usr/local/etc/openvswitch中找到它的数据库。如果你想将所有文件安装到/usr和/var中，而不是/usr/local和/usr/local/var中，并期望使用/etc/openvswitch作为默认数据库目录，请添加如下选项:

```
$ ./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc
```

OVS安装包像.rpm(例如通过yum安装或rpm -ivh)和.deb(例如通过apt-get安装或dpkg -i)使用上述配置选项。

默认情况下，会构建并链接静态库。如果你想使用共享库:

```
$ ./configure --enable-shared
```

你可以指定编译器：

```
$ ./configure CC=gcc-4.2
$ ./configure CC=clang
```

要向C编译器提供特殊标志，请在configure命令行中将它们指定为CFLAGS。如果希望使用默认的CFLAGS，其中包括用于构建调试符号的-g和用于启用优化的-O2，则必须自己包含它们。例如，要使用默认的CFLAGS plus -mssse3构建，您可以按如下方式运行configure：

```
$ ./configure CFLAGS="-g -O2 -mssse3"
```

为了提高哈希计算的效率，可以传递特殊的标志来利用内置的特性。例如，在支持SSE4.2指令集的X86_64上，可以通过传递-msse4.2来使用CRC32 intrinsics:

```
$ ./configure CFLAGS="-g -O2 -msse4.2"`
```

此外，内置的popcnt指令可以用来加快整数位集的计数。例如，在支持POPCNT的X86_64上，它可以通过传递-mpopcnt来启用:

```
$ ./configure CFLAGS="-g -O2 -march=native"
```

有了它，GCC将检测处理器并自动为它设置适当的标志。如果您在目标机器之外编译OVS，则不应使用此选项。

```
Note：
在构建Linux内核模块时不应用CFLAGS。内核模块的自定义CFLAGS是在运行make时使用EXTRA_CFLAGS变量提供的。例如:
$ make EXTRA_CFLAGS="-Wno-error=date-time"
```

如果您是一名开发人员，并且希望以大约2倍的运行时成本来启用Address Sanitizer功能，那么可以将-fsanitize= Address -fno- omt -frame-pointer -fno-common添加到CFLAGS中。例如:

```
$ ./configure CFLAGS="-g -O2 -fsanitize=address -fno-omit-frame-pointer -fno-common"
```

要构建Linux内核模块，以便能够运行基于内核的交换机，请在——with-linux上传递内核构建目录的位置。例如，要构建一个运行的Linux实例:

```
$ ./configure --with-linux=/lib/modules/$(uname -r)/build
```

如果——with- Linux请求构建一个不受支持的Linux版本，那么configure将失败并显示一条错误消息。有关这种情况的建议，请参阅Open vSwitch FAQ。

如果希望为构建所用机器的架构之外的架构构建内核模块，可以在调用configure脚本时使用KARCH变量指定内核架构字符串。例如，使用Linux构建MIPS:

```
$ ./configure --with-linux=/path/to/linux KARCH=mips
```

如果您计划进行大量的Open vSwitch开发，您可能想要添加——enable-Werror，它将-Werror选项添加到编译器命令行，将警告转换为错误。这使得不可能错过由构建生成的警告。例如:

```
$ ./configure --enable-Werror
```

如果您正在使用GCC进行构建，那么，要获得改进的警告，请安装sparse(请参阅“先决条件”)，并通过添加——enable-sparse来启用它。与——enable-Werror一起使用，以避免丢失编译器和**sparse**警告，例如:

```
$ ./configure --enable-Werror --enable-sparse
```

要使用gcov代码覆盖支持构建，请添加——enable-coverage:

```
$ ./configure --enable-coverage
```

configure脚本接受许多其他选项，并支持其他环境变量。对于完整的列表，使用——help选项invoke configure:

```
$ ./configure --help
```

您还可以从单独的构建目录运行configure。如果您希望从单个源目录以多种方式构建Open vSwitch，例如同时尝试GCC和Clang构建，或者为多个Linux版本构建内核模块，这是很有帮助的。例如:

```
$ mkdir _gcc && (cd _gcc && ./configure CC=gcc)
$ mkdir _clang && (cd _clang && ./configure CC=clang)
```

在某些情况下，使用jemalloc内存分配器而不是glibc内存分配器时，ovsdb-server和其他组件的性能会更好。如果你希望与jemalloc链接，请添加到LIBS:

```
$ ./configure LIBS=-ljemalloc
```

## 六、Building

1、在build目录下运行GNU make，例如:

```
$ make
```

如果GNU是用gmake安装的

```
$ gmake
```

如果你使用一个单独的构建目录，从该目录运行make或gmake，例如:

```
$ make -C _gcc
$ make -C _clang
```

有些版本的Clang和ccache不是完全兼容的。如果在一起使用时看到不寻常的警告，请考虑禁用ccache。

2、运行测试CASE，参考[Testing](http://docs.openvswitch.org/en/latest/topics/testing/)

3、运行make install将可执行文件和manpage安装到正在运行的系统中，默认情况下安装在/usr/local下：

```
$ make install
```

4、如果你构建了内核模块，可以这样安装他们：

```
$ make modules_install
```

您的机器上可能已经安装了一个来自上游Linux(在另一个目录中)的Open vSwitch内核模块。要确保加载从这个存储库构建的开放vSwitch内核模块，您应该创建一个depmod。选择新安装的内核模块而不是来自上游Linux的内核模块的d文件。下面的代码片段达到了同样的效果:

```
$ config_file="/etc/depmod.d/openvswitch.conf"
$ for module in datapath/linux/*.ko; do
  modname="$(basename ${module})"
  echo "override ${modname%.ko} * extra" >> "$config_file"
  echo "override ${modname%.ko} * weak-updates" >> "$config_file"
  done
$ depmod -a
```

最后，加载所需的内核模块。例如:

```
$ /sbin/modprobe openvswitch
```

要验证模块是否已加载，运行/sbin/lsmod并检查openvswitch是否存在

```
$ /sbin/lsmod | grep openvswitch
```

如果modprobe操作失败，请查看最后几条内核日志消息(例如，使用dmesg | tail)。通常，当Open vSwitch是为一个与您试图加载它的内核不同的内核构建的时候，会发生这样的问题。在openvswitch上运行modinfo。为运行中的内核构建的模块，例如:

```
$ /sbin/modinfo openvswitch.ko
$ /sbin/modinfo /lib/modules/$(uname -r)/kernel/net/bridge/bridge.ko
```

比较这两个命令输出的“vermagic”行。如果它们不同，那么Open vSwitch是为错误的内核构建的。

如果您决定报告一个bug或询问一个与模块加载相关的问题，请包括上面提到的dmesg和modinfo命令的输出。

## 七、Starting

在类似unix的系统(如BSDs和Linux)上，启动OpenvSwitch进程是一个简单的过程。Open vSwitch包含一个shell脚本和一个称为ovs-ctl的帮助程序，它可以自动化启动和停止ovsdb-server和ovs-vswitchd的大部分任务。安装之后，可以使用ovs-ctl实用程序启动守护进程。这将负责设置初始条件，并以正确的顺序启动守护进程。ovs-ctl实用程序位于' $(pkgdatadir)/scripts '中，默认设置为' /usr/local/share/openvswitch/scripts '。安装后的一个例子可能是:

```
$ export PATH=$PATH:/usr/local/share/openvswitch/scripts
$ ovs-ctl start
```

此外，ovs-ctl脚本允许使用特定的选项分别启动/停止守护进程。要启动ovsdb-server:

```
$ export PATH=$PATH:/usr/local/share/openvswitch/scripts
$ ovs-ctl --no-ovs-vswitchd start
```

同样地，先从ovs-vswitchd开始:

```
$ export PATH=$PATH:/usr/local/share/openvswitch/scripts
$ ovs-ctl --no-ovsdb-server start
```

除了使用自动脚本启动Open vSwitch之外，您可能还希望手动启动各种守护进程。在启动ovs-vswitchd本身之前，您需要启动它的配置数据库ovsdb-server。安装Open vSwitch的每台机器都应该运行自己的ovsdb-server副本。在ovsdb-server本身可以启动之前，配置一个它可以使用的数据库:

```
$ mkdir -p /usr/local/etc/openvswitch
$ ovsdb-tool create /usr/local/etc/openvswitch/conf.db \
    vswitchd/vswitch.ovsschema
```

配置ovsdb-server以使用上面创建的数据库，监听Unix域套接字，连接到数据库本身中指定的任何管理器，并在数据库中使用SSL配置:

```
$ mkdir -p /usr/local/var/run/openvswitch
$ ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
    --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
    --private-key=db:Open_vSwitch,SSL,private_key \
    --certificate=db:Open_vSwitch,SSL,certificate \
    --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
    --pidfile --detach --log-file
```

如果您在构建Open vSwitch时没有使用SSL支持，那么可以省略——private-key、——certificate和——bootstrap-ca-cert。

使用vs-vsctl初始化数据库。只有在使用ovsdb-tool创建数据库后的第一次才需要这样做，尽管在任何时候运行它都是无害的:

```
$ ovs-vsctl --no-wait init
```

启动主打开vSwitch守护进程，告诉它连接到相同的Unix域socket:

```
$ ovs-vswitchd --pidfile --detach --log-file
```

## 七、Validating

验证是否安装成功：

```
$ ovs-vsctl add-br br0
$ ovs-vsctl add-port br0 eth0
$ ovs-vsctl add-port br0 vif1.0
```

有关详细信息，请参阅ovs-vsctl(8)。您也可以参考 [Testing](http://docs.openvswitch.org/en/latest/topics/testing/)以获得关于OVS的更一般测试的信息。

当在容器中使用ovs时，exec to容器运行以上命令:

```
$ docker exec -it <ovsdb-server/ovs-vswitchd> /bin/bash
```


# 使用文档
CentOS7默认开启cgorupv2需要升级systemd版本，当前最靠谱的升级方式为Facebook维护的backports

## 0. 快速使用说明
打包好的rpm包在repo目录下，可以使用createrepo命令快速搭建自定义mirror
```bash
# 创建repodate
createrepo repo/
cd repo
# 启动http服务提供本地rpm源服务
nohup python -m SimpleHTTPServer &
cat << EOF | tee /etc/yum.repos.d/localhost
[localhost]
name=localhost
baseurl=http://127.0.0.1:8000/
enabled=1
gpgcheck=0
EOF
```

如果有自己打包的需求，参考步骤1到3可在CentOS7.9系统上复现，需要配置[epel repo](https://mirrors.ustc.edu.cn/help/epel.html)和[elrepo](http://elrepo.org/tiki/HomePage)


## 1. 安装并配置mock

### 工具包安装

```
yum install fedora-packager
```

### 自定义源配置

自定义源配置如下，==注意先启动本地rpm源服务==
```bash
cd /etc/mock
# 查看默认配置
mock]# cat default.cfg
include('templates/epel-7.tpl')

config_opts['root'] = 'epel-7-x86_64'
config_opts['target_arch'] = 'x86_64'
config_opts['legal_host_arches'] = ('x86_64',)

# 添加自定义源
cp templates/epel-7.tpl templates/epel-7.tpl.bak
cat << EOF | tee templates/epel-7.tpl
include('templates/centos-7.tpl')

config_opts['chroot_setup_cmd'] = 'install @buildsys-build'

config_opts['yum.conf'] += """
[localhost]
name=localhost
baseurl=http://127.0.0.1:8000/
enabled=1
gpgcheck=0

[epel]
name=Extra Packages for Enterprise Linux \$releasever - \$basearch
mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-7&arch=\$basearch
failovermethod=priority
gpgkey=file:///usr/share/distribution-gpg-keys/epel/RPM-GPG-KEY-EPEL-7
gpgcheck=1
skip_if_unavailable=False

[epel-testing]
name=Extra Packages for Enterprise Linux \$releasever - Testing - \$basearch
enabled=0
mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=testing-epel7&arch=\$basearch
failovermethod=priority
skip_if_unavailable=False

[local]
name=local
baseurl=https://kojipkgs.fedoraproject.org/repos/epel7-build/latest/\$basearch/
cost=2000
enabled=0
skip_if_unavailable=False

[epel-debuginfo]
name=Extra Packages for Enterprise Linux \$releasever - \$basearch - Debug
mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-debug-7&arch=\$basearch
failovermethod=priority
enabled=0
skip_if_unavailable=False
"""
EOF
```


## 2. 制作dependencies的rpm包
```
cd dependencies
mock --rebuild curl-7.49.0-1.fc25.src.rpm
cp /var/lib/mock/epel-7-x86_64/result/*.rpm repo
```

## 3. 制作backport rpm包

### 部分包的编译顺序有依赖

```
util-linux --> systemd-compat-libs
rpm-4.13.1 --> systemd

# 已不用编译python34的依赖，修改spec文件改用python36
# python34-cssselect --> python34-lxml --> systemd --> dbus-broker
```

### 编译命令
```
# 下载源代码
spectool -g -R rpms/systemd/specfiles/systemd.spec
# 打包src.rpm
rpmbuild -bs rpms/systemd/specfiles/systemd.spec
# 使用src.rpm打包二进制rpm
mock --rebuild /root/rpmbuild/SRPMS/systemd-246.1-1.fb7.src.rpm
```

## 4. 其他说明

### 4.1 包维护说明

|项目|说明|
|-|-|
|fedora历史版本src.rpm下载|https://koji.fedoraproject.org/koji/index|
|centos历史版本src.rpm下载|https://cbs.centos.org/koji/index|
|spec规范文档|https://docs.fedoraproject.org/en-US/packaging-guidelines/|

### 4.2 patch的使用




# Facebook backported RPMs for CentOS

Note: this repository is no longer being updated. See
[MIGRATION.md](MIGRATION.md) for more information.

This repo contains a number of RPM packages that we backported to CentOS 7 and 
run in our infrastructure. Most of these packages have dependencies from EPEL 
and from the last released CentOS 7 point release. Some packages also have 
extra dependencies from Fedora Rawhide that we list below. Because we pull from
Rawhide, some of these versions may no longer be available; in that case it's 
usually safe to use the latest release, but feel free to file an issue as well.
In our environment we import the `src.rpm` for these dependencies and rebuild
them in [mock](https://github.com/rpm-software-management/mock).

## Dependencies

`systemd` depends on the `dbus`, `python34-csselect`, `python34-lxml`, and
`util-linux` packages from this repo. It also requires the following packages
from Rawhide:
* curl-7.49.0-1.fc25
* dracut-044-75.fc25
* kmod-22-4.fc25
* libgudev-230-2.fc23

`mkosi` requires the following packages from Rawhide:
* arch-install-scripts-15-3.fc24
* archlinux-keyring-20160215-1.fc25
* debootstrap-1.0.81-1.fc24
* keyrings-filesystem-1-5.fc24
* python35-3.5.2-3.fc23

## Contribute

See the CONTRIBUTING file for how to help out.

## License

The RPM specfiles in this repository are released under the MIT license. See
LICENSE for more details.

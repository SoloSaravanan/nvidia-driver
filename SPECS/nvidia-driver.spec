# Feature: sign module
%define sign_module 1

%global kernel_rel %(dnf repoquery kernel-devel --latest-limit=1 --queryformat="%%{VERSION}-%%{RELEASE}")

%global main_rel %{autorelease}
%global module_rel %(dnf repoquery kernel-devel --latest-limit=1 --queryformat="%%{VERSION}")%{?dist}

%if %{sign_module}
%define sign_tool %(gzip -c %{SOURCE8} | base64)
%endif

%define module_dir kernel-open

%if 0%{?__isa_bits} == 64
%global elf_bits ()(64bit)
%endif

Name:                   nvidia-driver
Version:                615.71.09
Release:                %{main_rel}
Summary:                NVIDIA binary driver for Linux
Group:                  System Environment/Graphics
License:                LicenseRef-NVIDIA-Driver
URL:                    http://www.nvidia.com/
Source0:                https://in.download.nvidia.com/XFree86/Linux-%{_arch}/%{version}/NVIDIA-Linux-%{_arch}-%{version}.run
Source1:                https://in.download.nvidia.com/XFree86/Linux-%{_arch}/%{version}/NVIDIA-Linux-%{_arch}-%{version}.run.sha256sum

Source2:                nvidia.conf
Source3:                60-nvidia.conf
Source4:                31-nvidia-uvm.rules
Source5:                86-nvidia-driver.preset

%if %{sign_module}
Source8:                https://github.com/fxzxmic/sign-module/releases/download/v1.0.2/sign-module
%endif

BuildRequires:          gcc
BuildRequires:          make
BuildRequires:          kernel-devel = %{kernel_rel}
BuildRequires:          systemd-rpm-macros
BuildRequires:          jq
BuildRequires:          xz

%if %{sign_module}
# For sign-module utility
BuildRequires:          gzip
%endif

Requires:               nvidia-modprobe

Requires:               systemd

Suggests:               nvidia-smi

ExclusiveArch:          x86_64

%description
The NVIDIA Linux graphics driver.

%package -n nvidia-gpu-firmware
Summary:                NVIDIA Graphics firmware
Group:                  System Environment/Hardware

Epoch:                  1
BuildArch:              noarch

Provides:               nvidia-gpu-firmware = %{version}-%{main_rel}
Provides:               nvidia-gpu-firmware(gsp) = %{version}-%{main_rel}

%description -n nvidia-gpu-firmware
NVIDIA Graphics firmware

%package -n nvidia-common
Summary:                NVIDIA Graphics common files
Group:                  System Environment/Kernel

BuildArch:              noarch

Requires:               nvidia-modules-open = %{version}-%{main_rel}

Requires:               module-init-tools
Requires:               dracut

%description -n nvidia-common
NVIDIA Graphics common files

%package -n nvidia-modules-open
Summary:                NVIDIA Graphics kernel modules
Group:                  System Environment/Kernel
License:                MIT OR GPL-2.0-only

Release:                %{module_rel}

Requires:               kernel-uname-r = %{kernel_rel}.%{_arch}
Requires:               kernel-modules-core-uname-r = %{kernel_rel}.%{_arch}

Requires:               nvidia-gpu-firmware(gsp) = %{version}-%{main_rel}
Requires:               nvidia-common

%if %{sign_module}
# For sign-module utility
Requires(post):         %{_bindir}/base64
Requires(post):         %{_bindir}/gunzip
Requires(post):         libcrypto.so.3%{?elf_bits}
Requires(post):         liblzma.so.5%{?elf_bits}
Requires(post):         libc.so.6%{?elf_bits}
Requires(post):         libz.so.1%{?elf_bits}
%endif

Provides:               nvidia-modules-open-uname-r = %{kernel_rel}.%{_arch}
Provides:               nvidia-modules-open-%{_arch} = %{kernel_rel}
Provides:               installonlypkg(nvidia-modules-open)

Provides:               nvidia-modules-open = %{version}-%{main_rel}
Provides:               nvidia-modules-open%{?_isa} = %{version}-%{main_rel}

Supplements:            kernel-modules-uname-r = %{kernel_rel}.%{_arch}

Obsoletes:              nvidia-modules < %{version}

%description -n nvidia-modules-open
NVIDIA graphics kernel modules (Open Source Version)

%package -n nvidia-modprobe
Summary:                NVIDIA Modprobe Utility

Requires:               nvidia-modules-open%{?_isa} = %{version}-%{main_rel}

%description -n nvidia-modprobe
NVIDIA Modprobe Utility

%package -n nvidia-egl
Summary:                NVIDIA EGL Libraries

Requires:               %{name}%{?_isa} = %{version}-%{main_rel}

Requires:               (nvidia-gles%{?_isa} = %{version}-%{main_rel} if libGLES)

Requires:               vulkan-loader%{?_isa}
Requires:               libEGL%{?_isa}

Requires(post):         alternatives
Requires(preun):        alternatives

Supplements:            %{name}%{?_isa} = %{version}-%{main_rel}

%description -n nvidia-egl
NVIDIA EGL Libraries

%package -n nvidia-egl-wayland
Summary:                NVIDIA EGLStream Wayland Libraries
License:                MIT

Requires:               nvidia-egl%{?_isa} = %{version}-%{main_rel}

Conflicts:              egl-wayland

%description -n nvidia-egl-wayland
NVIDIA EGLStream Wayland Libraries (Deprecated)

%package -n nvidia-egl-gbm
Summary:                NVIDIA EGL GBM Libraries
License:                MIT

Requires:               nvidia-egl%{?_isa} = %{version}-%{main_rel}
Requires:               nvidia-gbm%{?_isa} = %{version}-%{main_rel}

Conflicts:              egl-gbm

%description -n nvidia-egl-gbm
NVIDIA EGL GBM Libraries

%package -n nvidia-egl-xwayland
Summary:                NVIDIA EGL XCB XLIB Libraries
License:                Apache-2.0

Requires:               nvidia-egl%{?_isa} = %{version}-%{main_rel}

Requires:               xorg-x11-server-Xwayland

Conflicts:              egl-x11

%description -n nvidia-egl-xwayland
NVIDIA EGL XCB XLIB Libraries

%package -n nvidia-smi
Summary:                NVIDIA System Management Interface

Requires:               nvidia-modprobe

%description -n nvidia-smi
NVIDIA System Management Interface

%package -n nvidia-gbm
Summary:                NVIDIA GBM Backend Libraries

Requires:               nvidia-modprobe

%description -n nvidia-gbm
NVIDIA GBM Backend Libraries

%package -n nvidia-gles
Summary:                NVIDIA GLES Libraries

Requires:               nvidia-modprobe

Requires:               libGLES%{?_isa}

%description -n nvidia-gles
NVIDIA GLES Libraries

%package -n nvidia-glx
Summary:                NVIDIA GLX Libraries

Requires:               %{name}%{?_isa} = %{version}-%{main_rel}
Requires:               nvidia-gbm%{?_isa} = %{version}-%{main_rel}

Requires:               vulkan-loader%{?_isa}
Requires:               libGL%{?_isa}

Requires(post):         alternatives
Requires(preun):        alternatives

Supplements:            %{name}%{?_isa} = %{version}-%{main_rel}

%description -n nvidia-glx
NVIDIA GLX Libraries

%package -n nvidia-vdpau
Summary:                NVIDIA VDPAU Libraries

Requires:               libvdpau.so.1%{?elf_bits}

%description -n nvidia-vdpau
NVIDIA VDPAU Libraries

%package -n nvidia-powerd
Summary:                NVIDIA Powerd Utilities

Requires:               nvidia-modprobe

Requires:               dbus
Requires:               systemd

%description -n nvidia-powerd
NVIDIA Powerd Utilities

%package -n nvidia-settings
Summary:                NVIDIA Settings Application

Requires:               %{name}%{?_isa} = %{version}-%{main_rel}
Requires:               nvidia-cfg%{?_isa} = %{version}-%{main_rel}

%description -n nvidia-settings
NVIDIA Settings Application

%package -n nvidia-ngx
Summary:                NVIDIA NGX Utilities

%description -n nvidia-ngx
NVIDIA NGX Utilities


%package -n nvidia-cfg
Summary:                NVIDIA Configuration Libraries

%description -n nvidia-cfg
NVIDIA Configuration Libraries

%package -n nvidia-utils
Summary:                NVIDIA Utilities

Requires:               %{name}%{?_isa} = %{version}-%{main_rel}

%description -n nvidia-utils
NVIDIA Utilities



%package -n nvidia-libs-32bit
Summary:                NVIDIA 32-bit shared libraries for compatibility
Requires:               nvidia-modprobe%{?_isa} = %{version}-%{main_rel}

%description -n nvidia-libs-32bit
Nvidia 32-bit libraries

%prep
cd %{_sourcedir}
# Verify sha256sum
sha256sum -c %{SOURCE1}

rm -rf %{_builddir}
sh %{SOURCE0} --extract-only --target %{_builddir}

%build
cd %{_builddir}/%{module_dir}
export SYSSRC=%{_prefix}/src/kernels/%{kernel_rel}.%{_arch}
export SYSOUT=$SYSSRC
export NV_EXCLUDE_KERNEL_MODULES="nvidia-vgpu-vfio nvidia-peermem"
%{make_build} modules

# Strip modules
strip --strip-unneeded *.ko

# Compress modules
xz --check=crc32 -9 *.ko

%install
mkdir -p %{buildroot}/lib/firmware/nvidia/%{version}
mkdir -p %{buildroot}%{_sysusersdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}-sleep
mkdir -p %{buildroot}%{_prefix}/lib/nvidia
mkdir -p %{buildroot}%{_libdir}/nvidia
mkdir -p %{buildroot}%{_libdir}/gbm
mkdir -p %{buildroot}%{_sysconfdir}/OpenCL/vendors
mkdir -p %{buildroot}%{_datadir}/dbus-1/system.d
mkdir -p %{buildroot}%{_datadir}/nvidia
mkdir -p %{buildroot}%{_datadir}/nvidia/vulkan
mkdir -p %{buildroot}%{_datadir}/vulkansc/icd.d
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_libdir}/vdpau
mkdir -p %{buildroot}/lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_libdir}/nvidia/wine
mkdir -p %{buildroot}/usr/lib/nvidia
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d
echo 'install_items+=" /lib/firmware/nvidia/%{version}/gsp_ga10x.bin /lib/firmware/nvidia/%{version}/gsp_tu10x.bin "' > %{buildroot}%{_sysconfdir}/dracut.conf.d/nvidia-firmware.conf

%if %{sign_module}
install -Dm0400 /dev/null -t %{buildroot}%{_sysconfdir}/keys/modsign.key
install -Dm0444 /dev/null -t %{buildroot}%{_sysconfdir}/keys/modsign.der
%endif
install -Dm0644 /dev/null -t %{buildroot}%{_datadir}/vulkan/icd.d/nvidia_icd.json
install -Dm0644 /dev/null -t %{buildroot}%{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json

mv firmware/* %{buildroot}/lib/firmware/nvidia/%{version}
mv nvidia-bug-report.sh %{buildroot}%{_bindir}
mv nvidia-modprobe %{buildroot}%{_bindir}
mv nvidia-modprobe.1.gz %{buildroot}%{_mandir}/man1
mv systemd/system/* %{buildroot}%{_unitdir}
mv systemd/system-sleep/* %{buildroot}%{_unitdir}-sleep
mv systemd/nvidia-sleep.sh %{buildroot}%{_bindir}
mv libglvnd_install_checker/* %{buildroot}%{_prefix}/lib/nvidia
mv nvidia-smi %{buildroot}%{_bindir}
mv nvidia-smi.1.gz %{buildroot}%{_mandir}/man1
mv libnvidia-ml.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-debugdump %{buildroot}%{_bindir}
mv libnvidia-gpucomp.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-api.so.* %{buildroot}%{_libdir}/nvidia
mv nvidia-dbus.conf %{buildroot}%{_datadir}/dbus-1/system.d
mv nvidia-powerd %{buildroot}%{_bindir}
mv libnvidia-glcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-tls.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia_icd.json %{buildroot}%{_datadir}/nvidia/vulkan
mv nvidia_layers.json %{buildroot}%{_datadir}/nvidia/vulkan
mv nvidia_icd_vksc.json %{buildroot}%{_datadir}/vulkansc/icd.d
mv nvidia-application-profiles-%{version}-* %{buildroot}%{_datadir}/nvidia
mv libGLX_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-present.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-tileiras.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-vksc-core.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glsi.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glvkspirv.so.%{version} %{buildroot}%{_libdir}/nvidia
mv 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mv libnvidia-eglcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libEGL_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libGLESv2_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libGLESv1_CM_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-egl-wayland.so.* %{buildroot}%{_libdir}/nvidia
mv libnvidia-egl-wayland2.so.* %{buildroot}%{_libdir}/nvidia
mv 09_nvidia_wayland2.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv 10_nvidia_wayland.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv libnvidia-egl-gbm.so.* %{buildroot}%{_libdir}/nvidia
mv 15_nvidia_gbm.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv libnvidia-egl-xcb.so.* %{buildroot}%{_libdir}/nvidia
mv 20_nvidia_xcb.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv libnvidia-egl-xlib.so.* %{buildroot}%{_libdir}/nvidia
mv 20_nvidia_xlib.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv nvidia-settings.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mv nvidia-settings %{buildroot}%{_bindir}
rm libnvidia-gtk2.so.%{version}
mv libnvidia-gtk3.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-wayland-client.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-settings.1.gz %{buildroot}%{_mandir}/man1
mv libnvidia-cfg.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau
mv libnvidia-allocator.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-rtcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-ngx.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-pcc %{buildroot}%{_bindir}
mv nvidia-ngx-updater %{buildroot}%{_bindir}
mv *.dll %{buildroot}%{_libdir}/nvidia/wine
chmod 755 %{buildroot}%{_libdir}/nvidia/wine/*.dll
mv libnvidia-fbc.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvcuvid.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-encode.so.%{version} %{buildroot}%{_libdir}/nvidia
rm libnvidia-pkcs11.so.%{version}
mv libnvidia-pkcs11-openssl3.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-sandboxutils.so.%{version} %{buildroot}%{_libdir}/nvidia
mv %{module_dir}/*.ko* %{buildroot}/lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video
mv nvidia-settings.desktop %{buildroot}%{_datadir}/applications
mv 32/libEGL_nvidia.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libGLESv1_CM_nvidia.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libGLESv2_nvidia.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libGLX_nvidia.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-eglcore.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-glcore.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-glvkspirv.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-gpucomp.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-tls.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-allocator.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-egl-gbm.so.1.1.3 %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-egl-wayland.so.1.1.20 %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-egl-wayland2.so.1.0.2 %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-egl-xcb.so.1.0.6 %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-egl-xlib.so.1.0.6 %{buildroot}/usr/lib/nvidia/
mv 32/libvdpau_nvidia.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvcuvid.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-fbc.so.%{version} %{buildroot}/usr/lib/nvidia/
mv 32/libnvidia-ml.so.%{version} %{buildroot}/usr/lib/nvidia/
echo "/usr/lib/nvidia" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/nvidia-32bit.conf

install -Dm0644 %{SOURCE2} -t %{buildroot}%{_modprobedir}
install -Dm0644 %{SOURCE3} -t %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d
install -Dm0644 %{SOURCE4} -t %{buildroot}%{_udevrulesdir}
install -Dm0644 %{SOURCE5} -t %{buildroot}%{_presetdir}

cp %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_icd.json %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_icd.json
cp %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_layers.json %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_layers.json
cp %{buildroot}%{_datadir}/vulkansc/icd.d/nvidia_icd_vksc.json %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_icd_vksc.json
cp %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_icd.json %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_icd_32.json

cp LICENSE LICENSE-%{version}-%{kernel_rel}
cp LICENSE LICENSE-%{version}

# Create symbolic links
cd %{buildroot}%{_libdir}
ln -sr nvidia/libnvidia-ml.so.%{version} libnvidia-ml.so.1
ln -sr nvidia/libnvidia-gpucomp.so.%{version} libnvidia-gpucomp.so.%{version}
ln -sr nvidia/libnvidia-api.so.* libnvidia-api.so.1
ln -sr nvidia/libnvidia-glcore.so.%{version} libnvidia-glcore.so.%{version}
ln -sr nvidia/libnvidia-tls.so.%{version} libnvidia-tls.so.%{version}
ln -sr nvidia/libGLX_nvidia.so.%{version} libGLX_nvidia.so.0
ln -sr libGLX_nvidia.so.0 libGLX_indirect.so.0
ln -sr nvidia/libnvidia-tileiras.so.%{version} libnvidia-tileiras.so.%{version}
ln -sr nvidia/libnvidia-present.so.%{version} libnvidia-present.so.%{version}
ln -sr nvidia/libnvidia-vksc-core.so.%{version} libnvidia-vksc-core.so.1
ln -sr nvidia/libnvidia-glsi.so.%{version} libnvidia-glsi.so.%{version}
ln -sr nvidia/libnvidia-glvkspirv.so.%{version} libnvidia-glvkspirv.so.%{version}
ln -sr nvidia/libnvidia-eglcore.so.%{version} libnvidia-eglcore.so.%{version}
ln -sr nvidia/libEGL_nvidia.so.%{version} libEGL_nvidia.so.0
ln -sr nvidia/libGLESv2_nvidia.so.%{version} libGLESv2_nvidia.so.2
ln -sr nvidia/libGLESv1_CM_nvidia.so.%{version} libGLESv1_CM_nvidia.so.1
ln -sr nvidia/libnvidia-egl-wayland.so.* libnvidia-egl-wayland.so.1
ln -sr nvidia/libnvidia-egl-wayland2.so.* libnvidia-egl-wayland2.so.1
ln -sr nvidia/libnvidia-egl-gbm.so.* libnvidia-egl-gbm.so.1
ln -sr nvidia/libnvidia-egl-xcb.so.* libnvidia-egl-xcb.so.1
ln -sr nvidia/libnvidia-egl-xlib.so.* libnvidia-egl-xlib.so.1
ln -sr nvidia/libnvidia-gtk3.so.%{version} libnvidia-gtk3.so.%{version}
ln -sr nvidia/libnvidia-wayland-client.so.%{version} libnvidia-wayland-client.so.%{version}
ln -sr nvidia/libnvidia-cfg.so.%{version} libnvidia-cfg.so.1
ln -sr vdpau/libvdpau_nvidia.so.%{version} vdpau/libvdpau_nvidia.so.1
ln -sr nvidia/libnvidia-allocator.so.%{version} libnvidia-allocator.so.1
ln -sr libnvidia-allocator.so.1 gbm/nvidia-drm_gbm.so
ln -sr nvidia/libnvidia-rtcore.so.%{version} libnvidia-rtcore.so.%{version}
ln -sr nvidia/libnvidia-ngx.so.%{version} libnvidia-ngx.so.%{version}
ln -sr libnvidia-ngx.so.%{version} libnvidia-ngx.so.1
ln -sr nvidia/libnvidia-fbc.so.%{version} libnvidia-fbc.so.1
ln -sr nvidia/libnvcuvid.so.%{version} libnvcuvid.so.1
ln -sr nvidia/libnvidia-encode.so.%{version} libnvidia-encode.so.1
ln -sr nvidia/libnvidia-pkcs11-openssl3.so.%{version} libnvidia-pkcs11-openssl3.so.%{version}
ln -sr nvidia/libnvidia-sandboxutils.so.%{version} libnvidia-sandboxutils.so.%{version}
ln -sr nvidia/libnvidia-sandboxutils.so.%{version} libnvidia-sandboxutils.so.1
ln -sr libnvidia-sandboxutils.so.1 libnvidia-sandboxutils.so

cd %{buildroot}/usr/lib
ln -sr nvidia/libGLX_nvidia.so.%{version} libGLX_nvidia.so.0
ln -sr nvidia/libEGL_nvidia.so.%{version} libEGL_nvidia.so.0
ln -sr nvidia/libGLESv2_nvidia.so.%{version} libGLESv2_nvidia.so.2
ln -sr nvidia/libnvidia-encode.so.%{version} libnvidia-encode.so.1


%check
ls -l * > %{_topdir}/leaves.list

%post
%systemd_post nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service nvidia-suspend-then-hibernate.service

%post -n nvidia-modules-open
%if %{sign_module}
if [ -f %{_sysconfdir}/keys/modsign.key ] && [ -f %{_sysconfdir}/keys/modsign.der ]; then
    chown root:root %{_sysconfdir}/keys/modsign.*
    chmod 400 %{_sysconfdir}/keys/modsign.key
    chmod 444 %{_sysconfdir}/keys/modsign.der
    base64 -d << EOF | gunzip > %{_tmppath}/sign-module
%{sign_tool}
EOF
    chmod +x %{_tmppath}/sign-module
    for module in /lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video/nvidia*.ko*; do
        %{_tmppath}/sign-module sha256 %{_sysconfdir}/keys/modsign.key %{_sysconfdir}/keys/modsign.der $module
    done
    rm -f %{_tmppath}/sign-module
fi
%endif
/sbin/depmod -a %{kernel_rel}.%{_arch}

%post -n nvidia-egl
update-alternatives --install %{_datadir}/vulkan/icd.d/nvidia_icd.json nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/egl-nvidia_icd.json 25 --follower %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json nvidia-vulkan-layers %{_datadir}/nvidia/vulkan/egl-nvidia_layers.json

%post -n nvidia-powerd
%systemd_post nvidia-powerd.service

%post -n nvidia-glx
update-alternatives --install %{_datadir}/vulkan/icd.d/nvidia_icd.json nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/nvidia_icd.json 50 --follower %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json nvidia-vulkan-layers %{_datadir}/nvidia/vulkan/nvidia_layers.json

%post -n nvidia-libs-32bit -p /sbin/ldconfig

%preun
%systemd_preun nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service nvidia-suspend-then-hibernate.service

%preun -n nvidia-egl
if [ $1 -eq 0 ]; then
    update-alternatives --remove nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/egl-nvidia_icd.json || :
fi

%preun -n nvidia-powerd
%systemd_preun nvidia-powerd.service

%preun -n nvidia-glx
if [ $1 -eq 0 ]; then
    update-alternatives --remove nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/nvidia_icd.json || :
fi

%postun
%systemd_postun nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service nvidia-suspend-then-hibernate.service

%postun -n nvidia-modules-open
/sbin/depmod -a %{kernel_rel}.%{_arch}

%postun -n nvidia-powerd
%systemd_postun nvidia-powerd.service

%postun -n nvidia-libs-32bit -p /sbin/ldconfig

%files
%license LICENSE
%doc README.txt
%doc NVIDIA_Changelog
%doc supported-gpus
%{_bindir}/nvidia-sleep.sh
%dir %{_libdir}/nvidia
%{_libdir}/nvidia/libnvidia-gpucomp.so.%{version}
%{_libdir}/libnvidia-gpucomp.so.%{version}
%{_libdir}/nvidia/libnvidia-api.so.*
%{_libdir}/libnvidia-api.so.1
%{_libdir}/nvidia/libnvidia-tls.so.%{version}
%{_libdir}/libnvidia-tls.so.%{version}
%{_libdir}/nvidia/libnvidia-glsi.so.%{version}
%{_libdir}/libnvidia-glsi.so.%{version}
%{_libdir}/nvidia/libnvidia-glvkspirv.so.%{version}
%{_libdir}/libnvidia-glvkspirv.so.%{version}
%{_unitdir}/nvidia-suspend.service
%{_unitdir}/nvidia-hibernate.service
%{_unitdir}/nvidia-resume.service
%{_unitdir}/nvidia-suspend-then-hibernate.service
%{_unitdir}/*/nvidia-suspend-nofreeze.conf
%{_unitdir}-sleep/*
%{_presetdir}/*
%{_udevrulesdir}/*
%dir %{_datadir}/nvidia
%dir %{_datadir}/nvidia/vulkan
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc

%files -n nvidia-gpu-firmware
%license LICENSE-%{version}
%dir /lib/firmware/nvidia
%dir /lib/firmware/nvidia/%{version}
/lib/firmware/nvidia/%{version}/*
%config %{_sysconfdir}/dracut.conf.d/nvidia-firmware.conf

%files -n nvidia-common
%config %{_modprobedir}/*
%config %{_prefix}/lib/dracut/dracut.conf.d/*
%if %{sign_module}
%dir %ghost %{_sysconfdir}/keys
%config(noreplace) %ghost %{_sysconfdir}/keys/*
%endif

%files -n nvidia-modules-open
%license LICENSE-%{version}-%{kernel_rel}
/lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video/*

%files -n nvidia-modprobe
%attr(4755,root,root) %{_bindir}/nvidia-modprobe
%{_mandir}/man1/nvidia-modprobe.1.gz

%files -n nvidia-egl
%{_libdir}/nvidia/libnvidia-eglcore.so.%{version}
%{_libdir}/libnvidia-eglcore.so.%{version}
%{_libdir}/nvidia/libEGL_nvidia.so.%{version}
%{_libdir}/libEGL_nvidia.so.0
%ghost %{_datadir}/vulkan/icd.d/nvidia_icd.json
%ghost %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json
%{_datadir}/glvnd/egl_vendor.d/*
%{_datadir}/nvidia/vulkan/egl-nvidia_icd.json
%{_datadir}/nvidia/vulkan/egl-nvidia_layers.json

%files -n nvidia-egl-wayland
%{_libdir}/nvidia/libnvidia-egl-wayland.so.*
%{_libdir}/libnvidia-egl-wayland.so.1
%{_libdir}/nvidia/libnvidia-egl-wayland2.so.*
%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json
%{_libdir}/libnvidia-egl-wayland2.so.1
%{_datadir}/egl/egl_external_platform.d/09_nvidia_wayland2.json

%files -n nvidia-egl-gbm
%{_libdir}/nvidia/libnvidia-egl-gbm.so.*
%{_libdir}/libnvidia-egl-gbm.so.1
%{_datadir}/egl/egl_external_platform.d/15_nvidia_gbm.json

%files -n nvidia-egl-xwayland
%{_libdir}/nvidia/libnvidia-egl-xcb.so.*
%{_libdir}/libnvidia-egl-xcb.so.1
%{_libdir}/nvidia/libnvidia-egl-xlib.so.*
%{_libdir}/libnvidia-egl-xlib.so.1
%{_datadir}/egl/egl_external_platform.d/20_nvidia_xcb.json
%{_datadir}/egl/egl_external_platform.d/20_nvidia_xlib.json

%files -n nvidia-smi
%attr(4755,root,root) %{_bindir}/nvidia-smi
%{_libdir}/nvidia/libnvidia-ml.so.%{version}
%{_libdir}/libnvidia-ml.so.1
%{_mandir}/man1/nvidia-smi.1.gz

%files -n nvidia-gbm
%{_libdir}/nvidia/libnvidia-allocator.so.%{version}
%{_libdir}/libnvidia-allocator.so.1
%dir %{_libdir}/gbm
%{_libdir}/gbm/*

%files -n nvidia-gles
%{_libdir}/nvidia/libGLESv2_nvidia.so.%{version}
%{_libdir}/libGLESv2_nvidia.so.2
%{_libdir}/nvidia/libGLESv1_CM_nvidia.so.%{version}
%{_libdir}/libGLESv1_CM_nvidia.so.1

%files -n nvidia-glx
%{_libdir}/nvidia/libGLX_nvidia.so.%{version}
%{_libdir}/libGLX_nvidia.so.0
%{_libdir}/nvidia/libnvidia-present.so.%{version}
%{_libdir}/libnvidia-present.so.%{version}
%{_libdir}/nvidia/libnvidia-tileiras.so.%{version}
%{_libdir}/libnvidia-tileiras.so.%{version}
%{_libdir}/nvidia/libnvidia-vksc-core.so.%{version}
%{_libdir}/libnvidia-vksc-core.so.1
%{_libdir}/libGLX_indirect.so.0
%{_libdir}/libnvidia-rtcore.so.%{version}
%{_libdir}/nvidia/libnvidia-rtcore.so.%{version}
%{_libdir}/nvidia/libnvidia-glcore.so.%{version}
%{_libdir}/libnvidia-glcore.so.%{version}
%ghost %{_datadir}/vulkan/icd.d/nvidia_icd.json
%ghost %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json
%{_datadir}/nvidia/vulkan/nvidia_icd.json
%{_datadir}/nvidia/vulkan/nvidia_layers.json
%{_datadir}/nvidia/vulkan/egl-nvidia_icd_vksc.json
%config(noreplace) %{_datadir}/vulkansc/icd.d/nvidia_icd_vksc.json

%files -n nvidia-vdpau
%{_libdir}/vdpau/*



%files -n nvidia-powerd
%{_bindir}/nvidia-powerd
%{_unitdir}/nvidia-powerd.service
%{_datadir}/dbus-1/system.d/*

%files -n nvidia-settings
%{_bindir}/nvidia-settings
%{_libdir}/nvidia/libnvidia-gtk3.so.%{version}
%{_libdir}/libnvidia-gtk3.so.%{version}
%{_libdir}/nvidia/libnvidia-wayland-client.so.%{version}
%{_libdir}/libnvidia-wayland-client.so.%{version}
%{_datadir}/icons/hicolor/**
%{_datadir}/applications/*
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation
%{_mandir}/man1/nvidia-settings.1.gz


%files -n nvidia-ngx
%{_bindir}/nvidia-pcc
%{_bindir}/nvidia-ngx-updater
%{_libdir}/nvidia/libnvidia-ngx.so.%{version}
%{_libdir}/libnvidia-ngx.so.%{version}
%{_libdir}/libnvidia-ngx.so.1
%{_libdir}/nvidia/wine/nvngx.dll
%{_libdir}/nvidia/wine/nvngx_dlssg.dll
%{_libdir}/nvidia/wine/_nvngx.dll


%files -n nvidia-cfg
%{_libdir}/nvidia/libnvidia-cfg.so.%{version}
%{_libdir}/libnvidia-cfg.so.1

%files -n nvidia-utils
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-debugdump
%dir %{_prefix}/lib/nvidia
%{_prefix}/lib/nvidia/*
%{_libdir}/nvidia/libnvcuvid.so.%{version}
%{_libdir}/nvidia/libnvidia-encode.so.%{version}
%{_libdir}/nvidia/libnvidia-fbc.so.%{version}
%{_libdir}/nvidia/libnvidia-pkcs11-openssl3.so.%{version}
%{_libdir}/nvidia/libnvidia-sandboxutils.so.%{version}
%{_libdir}/libnvidia-ml.so.1
%{_libdir}/vdpau/libvdpau_nvidia.so.1
%{_libdir}/libnvidia-encode.so.1
%{_libdir}/libnvcuvid.so.1
%{_libdir}/libnvidia-fbc.so.1
%{_libdir}/libnvidia-pkcs11-openssl3.so.%{version}
%{_libdir}/libnvidia-sandboxutils.so.%{version}
%{_libdir}/libnvidia-sandboxutils.so.1
%{_libdir}/libnvidia-sandboxutils.so


%files -n nvidia-libs-32bit
%dir /usr/lib/nvidia
/usr/lib/nvidia/lib*.so*
/usr/lib/libGLX_nvidia.so.0
/usr/lib/libEGL_nvidia.so.0
/usr/lib/libGLESv2_nvidia.so.2
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/nvidia-32bit.conf
%{_datadir}/nvidia/vulkan/nvidia_icd_32.json

%changelog
%{autochangelog}

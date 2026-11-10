**Go to the [Wiki](https://github.com/fxzxmicah/nvidia-driver/wiki/README) for details.**

**Add repository**

```
sudo sed -i '/^enabled=1$/!b; n; /^[[:space:]]*exclude=/!i exclude=*nvidia*' /usr/share/dnf5/repos.d/rpmfusion-nonfree*.repo

sudo tee -a /usr/share/dnf5/repos.d/nvidia-driver.repo > /dev/null << 'EOF'
[nvidia-driver]
name=Nvidia Driver
baseurl=https://solosaravanan.github.io/nvidia-driver/
enabled=1
gpgcheck=1
gpgkey=https://solosaravanan.github.io/nvidia-driver/pubkey.gpg
EOF
```

```
sudo dnf install -y \
  nvidia-driver \
  nvidia-gpu-firmware \
  nvidia-common \
  nvidia-modules-open \
  nvidia-modprobe \
  nvidia-egl \
  nvidia-egl-wayland \
  nvidia-egl-gbm \
  nvidia-egl-xwayland \
  nvidia-smi \
  nvidia-gbm \
  nvidia-gles \
  nvidia-glx \
  nvidia-vdpau \
  nvidia-powerd \
  nvidia-settings \
  nvidia-ngx \
  nvidia-cfg \
  nvidia-utils \
  nvidia-libs-32bit
```

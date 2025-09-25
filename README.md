**Go to the [Wiki](https://github.com/fxzxmicah/nvidia-driver/wiki/README) for details.**

**Add repository**

```
sudo tee -a /etc/yum.repos.d/nvidia-driver.repo > /dev/null << 'EOF'
[nvidia-driver]
name=Nvidia Driver
baseurl=https://solosaravanan.github.io/nvidia-driver/
enabled=1
gpgcheck=1
gpgkey=https://solosaravanan.github.io/nvidia-driver/pubkey.gpg
EOF
```

```
sudo dnf install -y nvidia-cfg nvidia-common nvidia-cuda nvidia-driver nvidia-egl nvidia-egl-gbm nvidia-egl-wayland nvidia-egl-xwayland nvidia-gbm nvidia-gles nvidia-glx nvidia-gpu-firmware nvidia-modprobe nvidia-modules-open nvidia-ngx>
```

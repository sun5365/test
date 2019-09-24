## 安装
- Windows系统

    1. 双击installer.bat安装依赖包
    2. 双击run.bat启动抽奖程序
   
- mac/Linux系统

    1. 安装Python2.7  
     
       mac: `brew install python2.7`  
       linux(ubuntu): `apt install python2.7`

    2. 安装pip

       mac: 完成第一步后自带pip
       linux(ubuntu): `apt install python2.7-pip` 

    3. 安装依赖包
   
       命令行运行`./install.sh`

    4. 启动程序

        命令行运行`./run.sh`

> 注意：本应用在抽奖过程中，会大量拉取人员头像。 在人员较多的情况下，请调整人员头像的大小尺寸，建议不要线上部署，如果是线上部署，请将静态文件部署至CDN
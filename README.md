# Nonebot_plugin_anti_flash
将收到的闪照发送给自己、指定qq或群组

## 配置项
`anti_flash_send_image`: `bool`
- 是否发送图片
- 默认值: `False`

`anti_flash_send_self`: `bool`
- 是否发送给自己
- 默认值: `False`

`anti_flash_send_user`: `List[int]`
- 发送qq号列表
- 默认值: `[]`
- 示例: `[123456789, 234567890]`

`anti_flash_send_group`: `List[int]`
- 发送群列表
- 默认值: `[]`
- 示例: `[12345678]`

`anti_flash_save_folder`: `Optional[str]`
- 将闪照保存到本地，留空则不保存
- 默认值: `None`
- 示例: `./data/flash/`

## 依赖
`nonebot2 >= 2.0.0beta.1` 
`nonebot-adapter-onebot >= 2.0.0-beta.1` 
`go-cqhttp == 1.0.0-rc1` 
`python-magic`

`libmagic1`:
- `pip install python-magic-bin` (Windows)
- `apt-get install libmagic1` (Debian/Ubuntu)
- `yum install file-devel` (Centos 7)


## 这有什么用
用自己的号挂上 go-cqhttp，收集群友的~~女装~~闪照
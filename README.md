# Nonebot_plugin_anti_flash
将收到的闪照发送给自己、指定qq或群组

## 配置项
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

## 依赖
`nonebot2 >= 2.0.0beta.1`
`nonebot-adapter-onebot >= 2.0.0-beta.1`
`go-cqhttp == 1.0.0-rc1`
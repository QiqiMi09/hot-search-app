▼ 接口信息
查询微博热门搜索榜单列表数据
接口地址：https://apis.tianapi.com/weibohot/index?key={apiKey} 
支持协议：http/https
请求方法：get/post
返回格式：utf-8 json
▼ 请求参数
上传文件时请使用标准表单格式 multipart/form-data
普通参数请使用默认表单格式 application/x-www-form-urlencoded
当参数值（如url、base64）包含特殊字符时，建议urlencode编码后传递
名称	类型	必须	示例值/默认值	说明
key	string	是	您自己的ApiKey（注册账号后获得）	API密钥
▼ 返回示例
接口数据示例仅作为预览参考，请以实际测试结果为准
旧接口域名返回的数据结构和现在略有不同，请查看说明
	
	
成功调用，返回内容并产生计费：

	{
  "msg": "success",
  "code": 200,
  "result": {
    "list": [
      {
        "hottag": "热",
        "hotword": "失踪女童确认曾在漳州出现",
        "hotwordnum": "129940"
      },
      {
        "hottag": "新",
        "hotword": "沈佳妮给朱亚文备注是大腻乎",
        "hotwordnum": "101845"
      },
      {
        "hottag": "热",
        "hotword": "为什么中国急着垃圾分类",
        "hotwordnum": "60143"
      },
      {
        "hottag": "热",
        "hotword": "闫桉宋雨琦好甜",
        "hotwordnum": "55388"
      },
      {
        "hottag": "新",
        "hotword": "WE现场加油声音被消音",
        "hotwordnum": "54237"
      }
    ]
  }
}

	
	
	
失败调用，查看接口错误码释义：

	{
  "code": 150,
  "msg": "API可用次数不足"
}

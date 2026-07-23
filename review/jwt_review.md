# JWT认证复习

## JWT vs Session

| 对比项 | Session | JWT |
|--------|---------|-----|
| 状态存储 | 服务端存Session | 客户端存Token |
| 扩展性 | 需要共享Session（Redis） | 无状态，天然支持分布式 |
| 注销 | 删除服务端Session即可 | 无法主动失效（需配合黑名单） |
| 适用场景 | 单体应用 | 微服务、API |

## 为什么JWT是安全的？

1. **签名验证**：服务端用密钥验证签名，确保Token未被篡改
2. **过期时间**：`exp`字段控制有效期
3. **HTTPS传输**：防止中间人窃取Token

## 常见攻击与防御

| 攻击方式 | 防御措施 |
|----------|----------|
| Token被窃取 | HTTPS + 短期有效期 + Refresh Token |
| CSRF | JWT存在localStorage而非Cookie |
| 签名绕过 | 强密钥 + 正确验证逻辑 |
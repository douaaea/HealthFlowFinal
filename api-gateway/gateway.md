classDiagram
direction BT
class ApiGatewayApplication {
  + ApiGatewayApplication() 
  + health() Map~String, String~
  + main(String[]) void
  + home() Map~String, Object~
}
class CorsConfig {
  + CorsConfig() 
  + corsWebFilter() CorsWebFilter
}
class GatewayConfig {
  + GatewayConfig() 
  + userKeyResolver() KeyResolver
}
class LoggingFilter {
  + LoggingFilter() 
  - Logger logger
  + filter(ServerWebExchange, GatewayFilterChain) Mono~Void~
  + getOrder() int
}
class RateLimitFilter {
  + RateLimitFilter() 
  - Map~String, AtomicInteger~ requestCounts
  - int MAX_REQUESTS_PER_MINUTE
  + filter(ServerWebExchange, GatewayFilterChain) Mono~Void~
  + getOrder() int
}


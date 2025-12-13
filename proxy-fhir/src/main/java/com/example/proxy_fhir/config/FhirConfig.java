package com.example.proxy_fhir.config;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import ca.uhn.fhir.rest.client.interceptor.LoggingInterceptor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FhirConfig {

    @Value("${hapi.fhir.server-url}")
    private String fhirServerUrl;

    @Bean
    public FhirContext fhirContext() {
        FhirContext ctx = FhirContext.forR4();

        // Configuration des timeouts
        ctx.getRestfulClientFactory().setConnectTimeout(30 * 1000);
        ctx.getRestfulClientFactory().setSocketTimeout(60 * 1000);

        return ctx;
    }

    @Bean
    public IGenericClient fhirClient(FhirContext fhirContext) {
        IGenericClient client = fhirContext.newRestfulGenericClient(fhirServerUrl);

        // Ajout d'un intercepteur de logging (optionnel)
        LoggingInterceptor loggingInterceptor = new LoggingInterceptor();
        loggingInterceptor.setLogRequestSummary(true);
        loggingInterceptor.setLogResponseSummary(true);
        client.registerInterceptor(loggingInterceptor);

        return client;
    }
}

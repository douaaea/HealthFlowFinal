package com.example.proxy_fhir.fhir.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.Map;

@Entity
@Table(name = "fhir_resources", indexes = {
        @Index(name = "idx_resource_type", columnList = "resource_type"),
        @Index(name = "idx_fhir_id", columnList = "fhir_id"),
        @Index(name = "idx_sync_date", columnList = "sync_date")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FhirResource {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "fhir_id", nullable = false, unique = true)
    private String fhirId;

    @Column(name = "resource_type", nullable = false, length = 50)
    private String resourceType;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "resource_data", nullable = false, columnDefinition = "jsonb")
    private Map<String, Object> resourceData;

    @Column(name = "version_id")
    private String versionId;

    @Column(name = "last_updated")
    private LocalDateTime lastUpdated;

    @Column(name = "sync_date", nullable = false)
    private LocalDateTime syncDate;

    @Column(name = "source_url")
    private String sourceUrl;

    @PrePersist
    protected void onCreate() {
        syncDate = LocalDateTime.now();
    }
}
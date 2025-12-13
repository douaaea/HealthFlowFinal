package com.example.proxy_fhir.fhir.repository;

import com.example.proxy_fhir.fhir.model.FhirResource;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface FhirResourceRepository extends JpaRepository<FhirResource, Long> {

    Optional<FhirResource> findByFhirId(String fhirId);

    List<FhirResource> findByResourceType(String resourceType);

    List<FhirResource> findBySyncDateAfter(LocalDateTime date);

    @Query("SELECT r.resourceType, COUNT(r) FROM FhirResource r GROUP BY r.resourceType")
    List<Object[]> countByResourceType();

    boolean existsByFhirId(String fhirId);
}
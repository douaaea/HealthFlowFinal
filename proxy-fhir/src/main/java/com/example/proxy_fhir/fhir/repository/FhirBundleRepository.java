package com.example.proxy_fhir.fhir.repository;

import com.example.proxy_fhir.fhir.model.FhirBundle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FhirBundleRepository extends JpaRepository<FhirBundle, Long> {

    List<FhirBundle> findByBundleType(String bundleType);
}
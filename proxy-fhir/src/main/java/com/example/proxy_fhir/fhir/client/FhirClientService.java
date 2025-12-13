package com.example.proxy_fhir.fhir.client;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import ca.uhn.fhir.rest.gclient.StringClientParam;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.hl7.fhir.r4.model.*;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class FhirClientService {

    private final IGenericClient fhirClient;
    private final FhirContext fhirContext;
    /**
     * Recherche tous les patients (avec limite)
     */
    public Bundle getAllPatients(int count) {
        log.info("Fetching {} patients from FHIR server", count);
        return fhirClient
                .search()
                .forResource(Patient.class)
                .count(count)
                .returnBundle(Bundle.class)
                .execute();
    }


    /**
     * Récupère un Patient par son ID
     */
    public Map<String, Object> getPatientById(String patientId) {
        log.info("Fetching Patient with ID: {}", patientId);

        Patient patient = fhirClient
                .read()
                .resource(Patient.class)
                .withId(patientId)
                .execute();

        return resourceToMap(patient);
    }

    /**
     * Recherche des Patients par critères
     */
    public Bundle searchPatients(Map<String, String> searchParams) {
        log.info("Searching Patients with params: {}", searchParams);

        var searchQuery = fhirClient
                .search()
                .forResource(Patient.class);

        // Ajout dynamique des paramètres de recherche
        searchParams.forEach((key, value) -> {
            searchQuery.where(new StringClientParam(key).matches().value(value));
        });

        return searchQuery.returnBundle(Bundle.class).execute();
    }

    /**
     * Récupère toutes les Observations d'un Patient
     */
    public Bundle getPatientObservations(String patientId) {
        log.info("Fetching Observations for Patient: {}", patientId);

        return fhirClient
                .search()
                .forResource(Observation.class)
                .where(Observation.SUBJECT.hasId(patientId))
                .returnBundle(Bundle.class)
                .execute();
    }

    /**
     * Récupère les Conditions (diagnostics) d'un Patient
     */
    public Bundle getPatientConditions(String patientId) {
        log.info("Fetching Conditions for Patient: {}", patientId);

        return fhirClient
                .search()
                .forResource(Condition.class)
                .where(Condition.SUBJECT.hasId(patientId))
                .returnBundle(Bundle.class)
                .execute();
    }

    /**
     * Récupère les MedicationRequests d'un Patient
     */
    public Bundle getPatientMedications(String patientId) {
        log.info("Fetching Medications for Patient: {}", patientId);

        return fhirClient
                .search()
                .forResource(MedicationRequest.class)
                .where(MedicationRequest.SUBJECT.hasId(patientId))
                .returnBundle(Bundle.class)
                .execute();
    }

    /**
     * Récupère un Bundle complet pour un Patient (tout son dossier)
     */
    public Bundle getPatientEverything(String patientId) {
        log.info("Fetching everything for Patient: {}", patientId);

        Parameters outParams = fhirClient
                .operation()
                .onInstance(new IdType("Patient", patientId))
                .named("$everything")
                .withNoParameters(Parameters.class)
                .execute();

        // Extraire le Bundle de la réponse
        return (Bundle) outParams.getParameter().get(0).getResource();
    }

    /**
     * Convertit une ressource FHIR en Map JSON
     */
    private Map<String, Object> resourceToMap(Resource resource) {
        IParser jsonParser = fhirContext.newJsonParser();
        String jsonString = jsonParser.encodeResourceToString(resource);

        // Conversion simple - pour une production, utiliser ObjectMapper
        Map<String, Object> map = new HashMap<>();
        map.put("resourceType", resource.getResourceType().name());
        map.put("id", resource.getIdElement().getIdPart());
        map.put("raw", jsonString);

        return map;
    }

    /**
     * Convertit un Bundle en Map JSON
     */
    public Map<String, Object> bundleToMap(Bundle bundle) {
        IParser jsonParser = fhirContext.newJsonParser();
        String jsonString = jsonParser.encodeResourceToString(bundle);

        Map<String, Object> map = new HashMap<>();
        map.put("type", bundle.getType().toCode());
        map.put("total", bundle.getTotal());
        map.put("resourceCount", bundle.getEntry().size());
        map.put("raw", jsonString);

        return map;
    }
}
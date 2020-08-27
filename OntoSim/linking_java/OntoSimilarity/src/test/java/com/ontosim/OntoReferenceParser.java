package com.ontosim;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.util.FileManager;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.fasterxml.jackson.databind.ObjectMapper;

/*
 * This file is for only parsing the reference file/ground truth
 */

public class OntoReferenceParser {

	public static void main(String[] args) throws IOException, ParseException {

		String baseDir = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/LargeBio_dataset_oaei2019/local_Gen/task_1_NCI_FMA/";
		
		String inputFileName = baseDir + "oaei_FMA2NCI_UMLS_mappings_with_flagged_repairs.rdf";

		String inputFileName_JSONLD = baseDir + "goldcopy.json";

		changeToJSONLD(inputFileName, inputFileName_JSONLD);

		String inputFileNameFinal_JSON = baseDir + "ontodata/output/goldcopy_final.json";

		readJson(inputFileName_JSONLD, inputFileNameFinal_JSON);

	}

	public static void changeToJSONLD(String inputFileName, String inputFileName_JSONLD) throws FileNotFoundException {

		// create an empty model
		Model model = ModelFactory.createDefaultModel();

		// use the FileManager to find the input file
		InputStream in = FileManager.get().open(inputFileName);

		// read the RDF/XML file
		model.read(in, "");

		// write it to standard out
		model.write(new FileOutputStream(new File(inputFileName_JSONLD)), "JSONLD");

	}

	public static void readJson(String inputFileName_JSON, String inputFileNameFinal_JSON)
			throws IOException, ParseException {

		List<OntoReferenceModel> ontoReferenceModelArr = new ArrayList<OntoReferenceModel>();
		JSONParser parser = new JSONParser();

		JSONObject main_obj = (JSONObject) parser.parse(new FileReader(inputFileName_JSON));
		JSONArray arr = (JSONArray) main_obj.get("@graph");

		for (int i = 0; i < arr.size(); i++) {
			try{
			JSONObject obj = (JSONObject) arr.get(i);
			OntoReferenceModel ontoReferenceModel = new OntoReferenceModel();
			ontoReferenceModel.setSrcKey(obj.get("alignmententity2").toString());
			ontoReferenceModel.setTargetKey(obj.get("alignmententity1").toString());
			ontoReferenceModelArr.add(ontoReferenceModel);
			}catch(Exception e){
				//escape any other entry
				continue;
			}
		}

		File file = new File(inputFileNameFinal_JSON);
		ObjectMapper mapper = new ObjectMapper();
		mapper.writerWithDefaultPrettyPrinter().writeValue(file, ontoReferenceModelArr);

	}

}

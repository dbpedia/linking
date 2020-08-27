package com.ontosim.cnst;

public interface OntoConst {
	
	String OntoThngCnst = "http://www.w3.org/2002/07/owl#Thing";
	String OntoNoThngCnst = "http://www.w3.org/2002/07/owl#Nothing";
	
	String OntoIntersectionOf = "ObjectIntersectionOf";
	String OntoUnionOff = "ObjectUnionOf";
	String OntoComplementOf = "ObjectComplementOf";
	String OntoOneOf = "ObjectOneOf";
	String OntoSomeValuesFrom = "ObjectSomeValuesFrom";
	String OntoAllValuesFrom = "ObjectAllValuesFrom";
	String OntoMinCardinality = "ObjectMinCardinality";
	String OntoMaxCardinality = "ObjectMaxCardinality";
	String OntoExactCardinality = "ObjectExactCardinality";
	String OntoHasValuef = "ObjectHasValue";
	
	String ERR = "Error Happened";
	String ERR_MSG_1 = "Input is blank";
	String ERR_MSG_2 = "Source file is missing";
	String ERR_MSG_3 = "Target file is missing";
	String ERR_MSG_4 = "Please select Data Source";
	String ERR_MSG_5 = "Error to call Python Web Service";
	
	String CLS_TYP = "Class";
	String OBJ_TYP = "ObjectProp";
	String DATA_TYP = "DataProp";
	
	String SRC = "source";
	String TRGT = "target";
	String SRC_FL = "source.json";
	String TRGT_FL = "target.json";
	String FL_EXT = ".json";
	String FL_TYP = "application/json";
	String SRC_IND = "src_file";
	String TRGT_IND = "trgt_file";
	
	String DS_1 = "Anatomy";
	String DS_2 = "LargeBio";
	
	String BASE_IND = "data:application/octet-stream;base64,";
	
	String PY_SERVICE_URL = "http://0.0.0.0:5000/OntoSimPyMain/ontorestservice/ontopy/task2";

}

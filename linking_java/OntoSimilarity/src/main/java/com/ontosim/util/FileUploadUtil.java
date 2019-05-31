package com.ontosim.util;

import org.apache.commons.fileupload.FileItem;

import com.ontosim.model.OntoFileModel;


public class FileUploadUtil {


	public OntoFileModel uploadFile(FileItem item, OntoFileModel ontoFlModel) throws Exception {

		ontoFlModel.setFileNm(item.getName());
		ontoFlModel.setFileIpStream(item.getInputStream());
		
		return ontoFlModel;
	}

}

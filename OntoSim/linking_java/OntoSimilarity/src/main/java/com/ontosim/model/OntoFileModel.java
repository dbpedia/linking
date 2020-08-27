package com.ontosim.model;

public class OntoFileModel {
	boolean isAvailable;
	String file_nm;
	String file_typ;
	String file;

	
	public boolean isAvailable() {
		return isAvailable;
	}

	public void setAvailable(boolean isAvailable) {
		this.isAvailable = isAvailable;
	}

	public String getFile_nm() {
		return file_nm;
	}

	public void setFile_nm(String file_nm) {
		this.file_nm = file_nm;
	}

	public String getFile_typ() {
		return file_typ;
	}

	public void setFile_typ(String file_typ) {
		this.file_typ = file_typ;
	}

	public String getFile() {
		return file;
	}

	public void setFile(String file) {
		this.file = file;
	}
}

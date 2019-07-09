package com.ontosim.model;

public class OntoServiceModel {

	OntoFileModel src_in_data;
	OntoFileModel trgt_in_data;
	OntoFileModel src_op_data;
	OntoFileModel trgt_op_data;
	OntoFileModel model;
	OntoFileMsg msg;
	
	public OntoFileModel getSrc_in_data() {
		return src_in_data;
	}
	public void setSrc_in_data(OntoFileModel src_in_data) {
		this.src_in_data = src_in_data;
	}
	public OntoFileModel getTrgt_in_data() {
		return trgt_in_data;
	}
	public void setTrgt_in_data(OntoFileModel trgt_in_data) {
		this.trgt_in_data = trgt_in_data;
	}
	public OntoFileModel getSrc_op_data() {
		return src_op_data;
	}
	public void setSrc_op_data(OntoFileModel src_op_data) {
		this.src_op_data = src_op_data;
	}
	public OntoFileModel getTrgt_op_data() {
		return trgt_op_data;
	}
	public void setTrgt_op_data(OntoFileModel trgt_op_data) {
		this.trgt_op_data = trgt_op_data;
	}
	public OntoFileModel getModel() {
		return model;
	}
	public void setModel(OntoFileModel model) {
		this.model = model;
	}
	public OntoFileMsg getMsg() {
		return msg;
	}
	public void setMsg(OntoFileMsg msg) {
		this.msg = msg;
	}

}

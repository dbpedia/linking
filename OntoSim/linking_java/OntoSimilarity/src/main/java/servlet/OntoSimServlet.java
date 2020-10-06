package servlet;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Base64;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import com.google.gson.Gson;
import com.ontosim.bl.OntoSimBL;
import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoDbModel;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoServiceModel;
import com.ontosim.util.OWLUtil;
import com.ontosim.util.OntoCallReqUtil;

/**
 * Servlet implementation class OntoSimServlet
 */
@WebServlet("/OntoSimServletUpload")
public class OntoSimServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

	OntoSimBL ontoSimBL = new OntoSimBL();
	OWLUtil owlUtil = new OWLUtil();
	OntoCallReqUtil ontoCallReqUtil = new OntoCallReqUtil();
	Gson gson = new Gson();
	Base64.Decoder dec = Base64.getDecoder();

	public OntoSimServlet() {
		super();
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		System.out.println("#################### Java OWL API START ####################");
		String retJSONStr = "";
		OutputStream os = null;

		if (ServletFileUpload.isMultipartContent(request)) {
			try {
				List<FileItem> multiparts = new ServletFileUpload(new DiskFileItemFactory()).parseRequest(request);

				OntoServiceModel ontoServiceModel = new OntoServiceModel();
				
				//Make it finalize before submit
				OntoDbModel ontoDbModel = new OntoDbModel();
				ontoDbModel.setDb_nm(OntoConst.DS_1);
				ontoDbModel.setVec_dim(OntoConst.vec_dim);
				ontoDbModel.setWord_wt_ds(OntoConst.word_wt_ds);
				ontoDbModel.setMeta_wt_ds(OntoConst.meta_wt_ds);
				ontoDbModel.setOp_k(OntoConst.op_k);
				ontoDbModel.setThreshold_ds(OntoConst.threshold_ds);
				
				ontoServiceModel.setDb(ontoDbModel);

				for (FileItem item : multiparts) {
					if (!item.isFormField()) {

						if (OntoConst.SRC_IND.equals(item.getFieldName())) {
							String srcBase64_Fl = ontoSimBL.ontoSimBL(item.getInputStream(), OntoConst.SRC);
							OntoFileModel src_in_data = new OntoFileModel();
							src_in_data.setFile(srcBase64_Fl);
							src_in_data.setFile_nm(OntoConst.SRC_FL);
							src_in_data.setFile_typ(OntoConst.FL_TYP);
							ontoServiceModel.setSrc_in_data(src_in_data);
						}

						if (OntoConst.TRGT_IND.equals(item.getFieldName())) {
							String trgtBase64_Fl = ontoSimBL.ontoSimBL(item.getInputStream(), OntoConst.TRGT);
							OntoFileModel trgt_in_data = new OntoFileModel();
							trgt_in_data.setFile(trgtBase64_Fl);
							trgt_in_data.setFile_nm(OntoConst.TRGT_FL);
							trgt_in_data.setFile_typ(OntoConst.FL_TYP);
							ontoServiceModel.setTrgt_in_data(trgt_in_data);
						}

					}
				}

				retJSONStr = owlUtil.convertFrmServiceModel(ontoServiceModel);

				retJSONStr = ontoCallReqUtil.ontoPOSTRequest(OntoConst.PY_SERVICE_URL, retJSONStr);

				ontoServiceModel = gson.fromJson(retJSONStr, OntoServiceModel.class);
				byte[] decbytes = dec.decode(ontoServiceModel.getFinal_op_data().getFile());

				InputStream is = new ByteArrayInputStream(decbytes);

				response.setContentType(ontoServiceModel.getFinal_op_data().getFile_typ());
				String headerKey = "Content-Disposition";
				String headerValue = String.format("attachment; filename=\"%s\"",
						ontoServiceModel.getFinal_op_data().getFile_nm());
				response.setHeader(headerKey, headerValue);
				os = response.getOutputStream();
				int i;
				while ((i = is.read()) != -1) {
					os.write(i);
				}

				is.close();
				os.close();

			} catch (Exception ex) {
				// Debugging purpose
				ex.printStackTrace();
			} finally {
				System.out.println("#################### Java OWL API STOP ####################");
			}

		}

	}

}

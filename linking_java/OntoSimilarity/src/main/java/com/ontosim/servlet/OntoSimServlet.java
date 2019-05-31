package com.ontosim.servlet;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileItemFactory;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import com.ontosim.bl.OntoSimBL;


@WebServlet("/OntoSimServlet")
public class OntoSimServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	OntoSimBL ontoSimBL = new OntoSimBL();
       

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		System.out.println("POST");
		
		// Set the response type and specify the boundary string
	    response.setContentType("multipart/x-mixed-replace;boundary=END");
	    // Set the content type based on the file type you need to download
	    String contentType = "Content-type: application/json";
	    ServletOutputStream out = response.getOutputStream();
	    
	 // Print the boundary string
	    out.println();
	    out.println("--END");

		boolean isMultipart = ServletFileUpload.isMultipartContent(request);

        if (isMultipart) {
            FileItemFactory factory = new DiskFileItemFactory();
            ServletFileUpload upload = new ServletFileUpload(factory);

            try {
                List items = upload.parseRequest(request);
                Iterator iterator = items.iterator();
                while (iterator.hasNext()) {
                    FileItem item = (FileItem) iterator.next();
                    List<File> fileLst = ontoSimBL.ontoSimBL(item);
                    
                    for(File file:fileLst){
                        FileInputStream fis = new FileInputStream(file);
                        BufferedInputStream bis = new BufferedInputStream(fis);
                        
                        
                        // Print the content type
                        out.println(contentType);
                        out.println("Content-Disposition: attachment; filename=" + file.getName());
                        out.println();
                        
                        int bytesRead = 0;
                        while ((bytesRead = bis.read()) != -1) {
                            out.write(bytesRead);
                        }
                        
                        bis.close();
                        fis.close();  
                        file = null;
                        
                        // Print the boundary string
                        out.println();
                        out.println("--END");
                    }
                }
            } catch (FileUploadException e) {
                e.printStackTrace();
            } catch (Exception e) {
                e.printStackTrace();
            }
            
            
            out.println("--END--");
            out.flush();
            out.close();
            
            RequestDispatcher rd=request.getRequestDispatcher("/index.html");  
            rd.include(request, response);
        }
	}

}

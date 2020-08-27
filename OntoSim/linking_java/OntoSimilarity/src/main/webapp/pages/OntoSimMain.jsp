<%@ page import="java.io.*,java.util.*,java.sql.*"%>
<%@ page import="javax.servlet.http.*,javax.servlet.*" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Ontology Alignment</title>
</head>
<body>

	<form action="OntoSimServletUpload" method="post" enctype="multipart/form-data">
		<table>
			<tr>
				<td>Source File:-</td>
				<td><input type="file" name="src_file" required/></td>
			</tr>
			<tr>
				<td>Target File:-</td>
				<td><input type="file" name="trgt_file" required/></td>
			</tr>
			<tr>
				<td colspan="2"><input type="submit" value="upload" /></td>
			</tr>
		</table>
	</form>

</body>
</html>

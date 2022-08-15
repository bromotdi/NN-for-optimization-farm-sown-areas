package project.controllers;

import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

import javax.servlet.RequestDispatcher;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.multipart.commons.CommonsMultipartFile;
import org.springframework.web.servlet.NoHandlerFoundException;

/**
 * @author Naberezhniy Artur
 * 
 * This is front controller.
 * It collects all requests to server and delegates them to other controllers.
 * FrontController doesn't have any logic in it, and only redirects requests
 * to pages and calling other controllers.
 */
@Controller
public class FrontController {
	private Map<String, String> messages;
	private static final Logger logger = LogManager.getLogger(FrontController.class);
	private HashMap<String, String> colors;
	
	@Autowired
	public FrontController() {
		messages = new HashMap<>();
		messages.put("403", "Access Denied");
		messages.put("404", "Page not Found");
		messages.put("500", "Server Exception");
		
		colors = new HashMap<>();
		colors.put("кукуруза", "#F7E78F");
		colors.put("жито", "#B6AD9E");
		colors.put("картопля рання", "#BCA796");
		colors.put("овес", "#F0E7D6");
		colors.put("ячмінь", "#E9DDC7");
		colors.put("пшениця", "#F6D294");
		colors.put("горох", "#EEFFAF");
		colors.put("люпин на зерно", "#90C1BB");
		colors.put("цукрові буряки", "#D5DEC9");
		colors.put("льон", "#F5DDFD");
		colors.put("соняшник", "#FFC72C");
		colors.put("пар", "#CEE2C7");
	}
	
	@GetMapping("/*")
	public void pageNotFound(HttpServletResponse response) throws IOException {
		response.sendRedirect("error?code=404");
	}
	
	@ExceptionHandler(Throwable.class)
    public void handleException(HttpServletResponse response, Throwable e) throws IOException {
        logger.error(e.getMessage(), e);
        response.sendRedirect("error?code=500");
    }
	
	@GetMapping("/error")
	public String getAccessDenied(HttpServletRequest request, Model model) {
		String code = request.getParameter("code");
		String message = messages.get(code);
		if (message == null)
			message = "";
		model.addAttribute("code", code);
		model.addAttribute("message", message);
		return "error";
	}
	
	@GetMapping("/home")
	public String getHome(HttpServletRequest request, Model model) {
		String result = (String) request.getSession().getAttribute("result");
		if (result != null && !result.isEmpty()) {
			String[] data = result.split(",");
			data[0] = data[0].substring(2);
			HashMap<String, Integer> count = new HashMap<>();
			String[] fields = new String[data.length - 1];
			for (int i = 0; i < data.length - 1; ++i) {
				count.put(data[i], count.getOrDefault(data[i], 0) + 1);
				fields[i] = colors.get(data[i]);
			}
			for (String i : count.keySet())
				count.put(i, (int)(count.get(i) / (data.length - 1f) * 100));
			
			HashMap<String, String[]> crops = new HashMap<>();
			for (String i : count.keySet())
				crops.put(i, new String[] {colors.get(i), String.valueOf(count.get(i))});
			
			model.addAttribute("crops", crops);
			model.addAttribute("fields", fields);
			model.addAttribute("profit", data[data.length - 1]);
		}
		
		return "index";
	}
	
	@PostMapping("/home")
	public void postData(@RequestParam CommonsMultipartFile file, HttpServletRequest request, HttpServletResponse response, Model model) {
		try {
			HttpSession session = request.getSession();
			
			String path=session.getServletContext().getRealPath("/");
			String filename=file.getOriginalFilename();
			filename = session.getId() + "." + filename.substring(filename.indexOf('.') + 1);
	        byte barr[]=file.getBytes();
	        BufferedOutputStream bout=new BufferedOutputStream(new FileOutputStream(path + "/input/" + filename));
	        bout.write(barr);
	        bout.flush();
	        bout.close();
	        
	        ProcessBuilder proc = new ProcessBuilder("C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python38\\python.exe", path + "main.py", filename);
	        Process process = proc.start();
	        InputStream in = process.getInputStream();
	        InputStream error = process.getErrorStream();
	        System.out.println(new String(error.readAllBytes()));
	        String res = new String(in.readAllBytes());
	        
	        session.setAttribute("result", res);
	        
	        response.sendRedirect("home");
		} catch(IOException e) {
			e.printStackTrace();
		}
	}
}

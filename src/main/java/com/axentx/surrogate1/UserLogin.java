package com.axentx.surrogate1;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class UserLogin extends HttpServlet {

    private static final Map<String, String> users = new HashMap<>();
    static {
        users.put("user1", "password1");
        users.put("admin", "admin123");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        HttpSession session = req.getSession();

        if (users.containsKey(username) && users.get(username).equals(password)) {
            session.setAttribute("username", username);
            resp.sendRedirect("/profile");
        } else {
            req.setAttribute("error", "Invalid username or password");
            req.getRequestDispatcher("/login.html").forward(req, resp);
        }
    }
}
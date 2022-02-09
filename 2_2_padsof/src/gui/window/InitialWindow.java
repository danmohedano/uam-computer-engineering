package gui.window;

import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.time.DateTimeException;
import java.time.LocalDate;

import javax.swing.*;

import application.Application;
import compositePattern.RegisteredCitizen;
import es.uam.eps.sadp.grants.CCGG;
import es.uam.eps.sadp.grants.InvalidIDException;
import exception.appExceptions.AlreadyLogInException;
import exception.projectExceptions.InvalidActionProjectException;
import modifiableDates.ModifiableDate;
import project.Project;
import project.Status;
/**
 * GUI for the Initial window, where users can register and login
 * @author Silvia Sopeña Niecko silvia.sopenna@estudiante.uam.es
 *
 */

public class InitialWindow extends JPanel implements ICard{
	
	private static final long serialVersionUID = 1L;
	private Login login;
	private Register register;
	private DateModifier date;
	private int x = 300;
	private int y = 320;
	
	ImageIcon icon = new ImageIcon("files/civium.png");	
	
	public InitialWindow(Window window) {
		login = new Login(window);
		register =  new Register(window);
		date = new DateModifier(window);
		this.setLayout(new BorderLayout());
		login.setBorder(BorderFactory.createTitledBorder("<html><b>Login</b></html>"));
		register.setBorder(BorderFactory.createTitledBorder("<html><b>Register</b></html>"));

		this.setBackground(Color.WHITE);

		this.add(login,  BorderLayout.WEST);
		this.add(register,  BorderLayout.EAST);
		this.add(date, BorderLayout.SOUTH);
	}
	
	
	@Override
	public int definedSizeY() {
		return y;
	}



	@Override
	public int definedSizeX() {
		return x;
	}



	@Override
	public JPanel getPanel() {
		return this;
	}
}

class Login extends JPanel {

		private static final long serialVersionUID = 1L;
		private JLabel logname, logpwd;
		private JTextField fieldlogname, fieldlogpwd;
		private JButton confirm = new JButton("Log In");

		public Login (Window window) {
		    SpringLayout layout = new SpringLayout();	
		    this.setLayout(layout); 
			this.setBackground(Color.WHITE);
		    // Components to be located ...
		    
			logname = new JLabel("<html><b>Name/ID</b></html>");
			fieldlogname = new JTextField(10);
			logpwd = new JLabel("<html><b>Password/ID</b></html>");
			fieldlogpwd = new JPasswordField(10);
			
	
		    
		    
	        //Login name 
		    
		    layout.putConstraint(SpringLayout.NORTH, logname, 5, SpringLayout.NORTH, this);
		    layout.putConstraint(SpringLayout.WEST, logname, 5, SpringLayout.WEST, this);
		    layout.putConstraint(SpringLayout.NORTH, fieldlogname, 5, SpringLayout.SOUTH, logname);
		    layout.putConstraint(SpringLayout.WEST, fieldlogname, 0, SpringLayout.WEST, logname);
		    //Login password
		    layout.putConstraint(SpringLayout.NORTH, logpwd, 10, SpringLayout.SOUTH, fieldlogname);
		    layout.putConstraint(SpringLayout.WEST, logpwd, 5, SpringLayout.WEST, this);
		    layout.putConstraint(SpringLayout.NORTH, fieldlogpwd, 5, SpringLayout.SOUTH, logpwd);
		    layout.putConstraint(SpringLayout.WEST, fieldlogpwd, 0, SpringLayout.WEST, logpwd);
		   
		    //Button
		    layout.putConstraint(SpringLayout.SOUTH, confirm, -5, SpringLayout.SOUTH, this);
		    layout.putConstraint(SpringLayout.WEST, confirm, 20, SpringLayout.WEST, fieldlogpwd);
		    
		    //add the components
		    this.add(logname); 
		    this.add(fieldlogname); 
		    this.add(logpwd); 
		    this.add(fieldlogpwd);
		    this.add(confirm);
		    this.confirm.addActionListener(new LoginMessage(window, this,fieldlogname, fieldlogpwd));
	
		    
		    this.setPreferredSize(new Dimension(140, 25));	// important: preferred size for this panel
		    this.setVisible(true);  
	    }
	}


class Register extends JPanel {

	private static final long serialVersionUID = 1L;
	private JLabel name, id, pwd;
	private JTextField fieldname, fieldid, fieldpwd;
	private JButton confirm = new JButton("Register");

	public Register (Window window) {
	    SpringLayout layout = new SpringLayout();	
	    this.setLayout(layout); 
		this.setBackground(Color.WHITE);
	
	    // Components to be located ...
		
		name = new JLabel("<html><b>Name</b></html>");
		fieldname = new JTextField(10);
		id = new JLabel("<html><b>ID</b></html>");
		fieldid = new JTextField(10);
		pwd = new JLabel("<html><b>Password</b></html>");
		fieldpwd = new JPasswordField(10);
	
		
	       
	    //Register name
		layout.putConstraint(SpringLayout.NORTH, name, 5, SpringLayout.NORTH, this);
	    layout.putConstraint(SpringLayout.WEST, name, 5, SpringLayout.WEST, this);
	    layout.putConstraint(SpringLayout.NORTH, fieldname, 5, SpringLayout.SOUTH, name);
	    layout.putConstraint(SpringLayout.WEST, fieldname, 0, SpringLayout.WEST, name);
	    //Login password
	    layout.putConstraint(SpringLayout.NORTH, id, 10, SpringLayout.SOUTH, fieldname);
	    layout.putConstraint(SpringLayout.WEST, id, 0, SpringLayout.WEST, fieldname);
	    layout.putConstraint(SpringLayout.NORTH, fieldid, 5, SpringLayout.SOUTH, id);
	    layout.putConstraint(SpringLayout.WEST, fieldid, 0, SpringLayout.WEST, id);
	    
	    layout.putConstraint(SpringLayout.NORTH, pwd, 10, SpringLayout.SOUTH, fieldid);
	    layout.putConstraint(SpringLayout.WEST, pwd, 0, SpringLayout.WEST, fieldid);
	    layout.putConstraint(SpringLayout.NORTH, fieldpwd, 5, SpringLayout.SOUTH, pwd);
	    layout.putConstraint(SpringLayout.WEST, fieldpwd, 0, SpringLayout.WEST, pwd);
	   
	    //Button
	    layout.putConstraint(SpringLayout.SOUTH, confirm, -5, SpringLayout.SOUTH, this);
	    layout.putConstraint(SpringLayout.WEST, confirm, 20, SpringLayout.WEST, fieldpwd);
	    
	    //add the components
	    this.add(name); 
	    this.add(fieldname); 
	    this.add(id);
	    this.add(fieldid);
	    this.add(pwd); 
	    this.add(fieldpwd);
	    this.add(confirm);
	    this.confirm.addActionListener(new RegisterMessage(window, this, fieldname, fieldid, fieldpwd));
	    
	    this.setPreferredSize(new Dimension(140,100));
	    this.setVisible(true);  
    }
}
	
	
class LoginMessage implements ActionListener {
	
	private Component ventana;
	JTextField fieldlog;
	JTextField fieldpwd;
	Window window;

	public LoginMessage(Window window, Component ventana, JTextField fieldlog, JTextField fieldpwd) {
		this.window = window;
		this.ventana = ventana;
		this.fieldlog = fieldlog;
		this.fieldpwd = fieldpwd;
	}

	public void actionPerformed(ActionEvent e) {

		if (fieldlog.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(ventana, "Write a valid Name or ID");
			return;
		}
		else if(fieldpwd.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(ventana, "Write a valid password");
			return;
		}
		
		else {
			try {
				if(Application.login(fieldlog.getText(), fieldpwd.getText()) == false) {
					RegisteredCitizen doesexist = RegisteredCitizen.getCitizenByName(fieldlog.getText());
					if(doesexist != null) {
						if(doesexist.getBan() == true) JOptionPane.showMessageDialog(ventana, "You're banned");
						else JOptionPane.showMessageDialog(ventana, "You haven't been accepted yet");
					}
					else JOptionPane.showMessageDialog(ventana, "Password, id or name wrong");
					return;
				}
			} catch (AlreadyLogInException e1) {
				JOptionPane.showMessageDialog(ventana, "How the fuck did you do this");
				JOptionPane.showMessageDialog(ventana, e1);

			}
			
			//Look for out of date projects and check for funding of the projects
			for (Project p : Project.getAllProjects()) {
				p.checkDls();
				if (p.getStatus().equals(Status.WAITING)) {
						try {
							p.receiveFunding();
						} catch (InvalidActionProjectException | IOException | InvalidIDException e1) {
							e1.printStackTrace();
						}
				}
			}
			
			window.setLoggedin(true);
			window.showPanel(null);
			return;
		}


		}
	}

class RegisterMessage implements ActionListener {
	
	private Component ventana;
	JTextField fieldname;
	JTextField fieldid;
	JTextField fieldpwd;
	CardLayout generalPanel;
	Window window;
	public RegisterMessage(Window window, Component ventana, JTextField fieldname, JTextField fieldid, JTextField fieldpwd) {
		this.window = window;
		this.ventana = ventana;
		this.fieldname = fieldname;
		this.fieldid = fieldid;
		this.fieldpwd = fieldpwd;
	}

	public void actionPerformed(ActionEvent e) {

		if (fieldname.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(ventana, "Write a valid Name");
			return;
		}
		
		if (fieldid.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(ventana, "Write a valid ID");
			return;
		}
		
		else if(fieldpwd.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(ventana, "Write a valid password");
			return;
		}
		
		else {
			try {
				new RegisteredCitizen(fieldname.getText(), fieldpwd.getText(), fieldid.getText(), false);
				JOptionPane.showMessageDialog(ventana,"Registered Successfully");

				return;

			} catch (Exception e1) {
				JOptionPane.showMessageDialog(ventana,e1);
				
			}
			
			
		}


		}
	}

@SuppressWarnings("serial")
class DateModifier extends JPanel{
	private JTextField day = new JTextField(Integer.toString(ModifiableDate.getModifiableDate().getDayOfMonth()), 7);
	private JTextField month = new JTextField(Integer.toString(ModifiableDate.getModifiableDate().getMonthValue()), 7);
	private JTextField year = new JTextField(Integer.toString(ModifiableDate.getModifiableDate().getYear()), 7);
	private JButton setDate = new JButton("Set Date");
	private JButton today = new JButton("Use Today");
	
	
	public DateModifier(Window window) {
		SpringLayout s = new SpringLayout();
		this.setLayout(s);
		this.setBorder(BorderFactory.createTitledBorder("<html><b>Choose a date to simulate</b></html>"));
		this.setBackground(Color.WHITE);
		
		s.putConstraint(SpringLayout.NORTH, this.day, 5, SpringLayout.NORTH, this);
		s.putConstraint(SpringLayout.WEST, this.day, 5, SpringLayout.WEST, this);
		s.putConstraint(SpringLayout.NORTH, this.month, 5, SpringLayout.NORTH, this);
		s.putConstraint(SpringLayout.WEST, this.month, 5, SpringLayout.EAST, this.day);
		s.putConstraint(SpringLayout.NORTH, this.year, 5, SpringLayout.NORTH, this);
		s.putConstraint(SpringLayout.WEST, this.year, 5, SpringLayout.EAST, this.month);
		s.putConstraint(SpringLayout.NORTH, this.setDate, 5, SpringLayout.SOUTH, this.day);
		s.putConstraint(SpringLayout.WEST, this.setDate, 5, SpringLayout.WEST, this);
		s.putConstraint(SpringLayout.NORTH, this.today, 5, SpringLayout.SOUTH, this.year);
		s.putConstraint(SpringLayout.EAST, this.today, 0, SpringLayout.EAST, this.year);
		
		
		this.add(this.day); this.add(this.month); this.add(this.year); this.add(this.setDate); this.add(this.today);
		this.setDate.addActionListener(new SetDateListener(window, this.day, this.month, this.year));
		this.today.addActionListener(new SetTodayListener(window, this.day, this.month, this.year));
		this.setPreferredSize(new Dimension(250, 100));
	}
}

class SetDateListener implements ActionListener{
	private Window window;
	private JTextField day;
	private JTextField month;
	private JTextField year;
	
	public SetDateListener(Window window, JTextField day, JTextField month, JTextField year) {
		this.window = window;
		this.day = day;
		this.month = month;
		this.year = year;
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		int nday, nmonth, nyear;
		try {
			nday = Integer.parseInt(this.day.getText());
			nmonth = Integer.parseInt(this.month.getText());
			nyear = Integer.parseInt(this.year.getText());
		}catch(NumberFormatException e1) {
			JOptionPane.showMessageDialog(this.window, "Must enter a valid date");
			return;
		}
		try {
			@SuppressWarnings("unused")
			LocalDate test = LocalDate.now().withDayOfMonth(nday).withMonth(nmonth).withYear(nyear);
		}catch(DateTimeException e2){
			JOptionPane.showMessageDialog(this.window, "Must enter a valid date");
			return;
		}
		ModifiableDate.setDate(nday, nmonth, nyear);
		CCGG.getGateway().setDate(ModifiableDate.getModifiableDate());
		JOptionPane.showMessageDialog(this.window, "Correctly set the date.");
	}
	
}

class SetTodayListener implements ActionListener{
	private Window window;
	private JTextField day;
	private JTextField month;
	private JTextField year;
	
	public SetTodayListener(Window window, JTextField day, JTextField month, JTextField year) {
		this.window = window;
		this.day = day;
		this.month = month;
		this.year = year;
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		ModifiableDate.setToday();
		CCGG.getGateway().setDate(ModifiableDate.getModifiableDate());
		this.day.setText(Integer.toString(ModifiableDate.getModifiableDate().getDayOfMonth()));
		this.month.setText(Integer.toString(ModifiableDate.getModifiableDate().getMonthValue()));
		this.year.setText(Integer.toString(ModifiableDate.getModifiableDate().getYear()));
		JOptionPane.showMessageDialog(this.window, "Correctly set the date.");
	}
	
}



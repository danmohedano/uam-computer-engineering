package gui.user;


import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;

import project.Project;

import javax.swing.*;

import application.Admin;
import gui.window.Window;


/**
 * class for the Admin to accept or reject projects
 * @author Silvia Sope�a Niecko silvia.sopenna@estudiante.uam.es
 *
 */
public class AdminAcceptReject extends JFrame{
	
	private static final long serialVersionUID = 1L;
	private JLabel text;
	ImageIcon yes = new ImageIcon("files/yes.png");
	ImageIcon no = new ImageIcon("files/no.png");
	private JButton accept = new JButton(yes);
	private JButton reject = new JButton(no);
	private Project p;
	public AdminAcceptReject(Window window, String name) {
		text = new JLabel("Accept Project " + name + "?");
		this.p = Project.getProject(name);
		this.setBackground(Color.WHITE);
		Container cp = this.getContentPane();
		cp.setBackground(Color.WHITE);
		SpringLayout layout = new SpringLayout();	
	    cp.setLayout(layout); 
	    Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
	    this.setLocation(dim.width/2-this.getSize().width/2, dim.height/2-this.getSize().height/2);
	    
		Font f = new Font(text.getFont().getFontName(), Font.BOLD, 24);
		text.setFont(f);

	    layout.putConstraint(SpringLayout.NORTH, text, 5, SpringLayout.NORTH, this);
	    layout.putConstraint(SpringLayout.WEST, text, 5, SpringLayout.WEST, this);
	    
	    layout.putConstraint(SpringLayout.WEST, accept, 10, SpringLayout.WEST, this);
	    layout.putConstraint(SpringLayout.NORTH, accept, 5, SpringLayout.SOUTH, text);
	    layout.putConstraint(SpringLayout.WEST, reject, 5, SpringLayout.EAST, accept);
	    layout.putConstraint(SpringLayout.NORTH, reject, 0, SpringLayout.NORTH, accept);
	    
	    
		cp.add(text);
		cp.add(accept);
		cp.add(reject);
		this.accept.addActionListener(new AcceptMessage(this, window, p));
		this.reject.addActionListener(new RejectMessage(this, window, p));
		this.setSize(10*name.length()+300,125);
		this.setResizable(false);
		this.setVisible(true);

	}
	
	

}

class AcceptMessage implements ActionListener {

	private Window window;
	private Project p;
	private JFrame frame;

	public AcceptMessage(JFrame frame, Window window, Project p) {
		this.window = window;
		this.p = p;
		this.frame = frame;
		
	}

	public void actionPerformed(ActionEvent e) {
		
		JOptionPane.showMessageDialog(window, "The project has been accepted.");
		Admin.validate(p, true, null);
		frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));
		window.showPanel(new AdminsProfile(window));

	}
}

class RejectMessage implements ActionListener {
	
		private Project p;
		private JFrame frame;
		private Window window;
	public RejectMessage(JFrame frame, Window window,Project p) {
		this.window = window;
		this.p = p;
		this.frame = frame;
	}

	public void actionPerformed(ActionEvent e) {

		new Motivation(window, p);
		frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));


	}
}
package gui.user;


import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;

import project.Project;

import javax.swing.*;

import application.Admin;
import gui.window.Window;


/**
 * Motivation of the rejected project
 * @author Silvia Sope�a Niecko silvia.sopenna@estudiante.uam.es
 *
 */
public class Motivation extends JFrame{
	
	private static final long serialVersionUID = 1L;
	private JLabel text;
	private JTextArea motivation;
	private JButton send = new JButton("Send motivation");
	
	public Motivation(Window window, Project p) {
		
		text = new JLabel("You have rejected" + p.getName() + "." + "Please, write down the reason.");
		
		motivation = new JTextArea();
		motivation.setLineWrap(true);
		motivation.setWrapStyleWord(true);
		
		Container cp = this.getContentPane();
		BorderLayout layout = new BorderLayout();	
		text.setFont(new Font(cp.getFont().getFontName(), Font.BOLD, 13));
		cp.setLayout(layout); 
    
		cp.add(text, BorderLayout.NORTH);
		cp.add(motivation, BorderLayout.CENTER);
		cp.add(send, BorderLayout.SOUTH);
		send.addActionListener(new sendMotivation(this, p, motivation, window));
		
		this.setBackground(Color.WHITE);
		this.setSize(550,250);
		this.setVisible(true);
	}
	
	
	class sendMotivation implements ActionListener {
		
		private Project p;
		private JTextArea text;
		private JFrame frame;
		private Window window;
		public sendMotivation(JFrame frame, Project p, JTextArea text, Window window) {
			this.window = window;
			this.p = p;
			this.text = text;
			this.frame = frame;
		}
	
		public void actionPerformed(ActionEvent e) {
	
			Admin.validate(p, false, text.getText());
			window.showPanel(new AdminsProfile(window));
			frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));
				
		}
	
	

}


}
/**
 * 
 */
package gui.user;

import java.awt.BorderLayout;
import java.awt.Color;

import javax.swing.*;

import application.Application;
import notification.Notification;

/**
 * User's Notifications class
 * @author Silvia Sopeña Niecko silvia.sopenna@estudiante.uam.es
 *
 */
public class UsersNotifications extends JFrame{
	
	private static final long serialVersionUID = 1L;
	DefaultListModel<String> List= new DefaultListModel<String>();				
	JList<String> list= new JList<String>(List);
	
	
	public UsersNotifications() {
		
		for(Notification n: Application.currentuser.getNotification()) {
			if (n.isRead() == false) {
				List.addElement(n.toString());
				n.setRead(true);
			}
		}
		this.setBackground(Color.WHITE);
		this.setLayout(new BorderLayout());
		JScrollPane scrollbar= new JScrollPane(list);
		list.setLayoutOrientation(JList.VERTICAL);
		list.setVisibleRowCount(10);
		this.add(scrollbar, BorderLayout.NORTH);	
		
		this.setTitle("User's Notifications");
		this.setSize(500,200);
		this.setResizable(false);
		this.setVisible(true);
	}

}

package gui.user;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import application.Application;
import compositePattern.Group;
import gui.group.GroupScreen;
import gui.project.ProjectScreen;
import gui.window.ICard;
import gui.window.Window;
import project.Project;


/**
 * GUI for the Users Profile class
 * @author Silvia Sopeña Niecko silvia.sopenna@estudiante.uam.es
 * 
 */

public class UsersProfile extends JPanel implements ICard {

	private static final long serialVersionUID = 1L;
	
	private NorthLayout north = new NorthLayout(null);
	private GP south;
	private int x = 325;
	private int y = 320;
	public UsersProfile(Window window) {
		south = new GP(window);
		this.setBackground(Color.WHITE);
		SpringLayout layout = new SpringLayout();
		this.setLayout(layout);
		layout.putConstraint(SpringLayout.NORTH, north, 5, SpringLayout.NORTH, this);
		layout.putConstraint(SpringLayout.WEST, north, 5, SpringLayout.WEST, this);	
		this.add(north);
		layout.putConstraint(SpringLayout.NORTH, south, 5, SpringLayout.SOUTH, north);
		layout.putConstraint(SpringLayout.WEST, south, 5, SpringLayout.WEST, this);	
		this.add(south);
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

class NorthLayout extends JPanel {
	
	private static final long serialVersionUID = 1L;
	
	ImageIcon noNotIcon = new ImageIcon("files/noNotIcon.png");
	ImageIcon notIcon = new ImageIcon("files/notIcon.png");	
	
	private JLabel user = new JLabel(Application.currentuser.getName() + "'s profile");
	private JButton notification = new JButton("");
	
	DefaultListModel<String> GList= new DefaultListModel<String>();				
	
	public NorthLayout(Window window) {
		Font f = new Font(user.getFont().getFontName(), Font.BOLD, 24);
		user.setFont(f);
		this.setBackground(Color.WHITE);
		notification.setPreferredSize(new Dimension(50, 50));
		this.setLayout(new BorderLayout());
	    this.notification.setIcon(notIcon);
	    this.add(notification);
	    this.notification.addActionListener(new Notification(this, notification, notIcon, noNotIcon));
	    
		this.add(user,  BorderLayout.CENTER);
		this.add(notification,  BorderLayout.EAST);
		
		
	    this.setPreferredSize(new Dimension(300, 50));	
	    this.setVisible(true); 
	}
	

}


class GP extends JPanel {
	
	private static final long serialVersionUID = 1L;
	
	private GroupPanel g;
	private ProjectPanel p;


	
	public GP(Window window) {
		p = new ProjectPanel(window);
		g = new GroupPanel(window);
		this.setLayout(new BorderLayout());
		g.setBorder(BorderFactory.createTitledBorder("<html><b>Groups</b></html>"));
		p.setBorder(BorderFactory.createTitledBorder("<html><b>Projects</b></html>"));

		this.setBackground(Color.WHITE);
		this.add(g, BorderLayout.WEST);
		this.add(p,  BorderLayout.EAST);
		
	    this.setPreferredSize(new Dimension(300, 250));	
	    this.setVisible(true); 
	}
	

}


class GroupPanel extends JPanel {

		private static final long serialVersionUID = 1L;
		
		DefaultListModel<String> GList= new DefaultListModel<String>();				
		JList<String> list= new JList<String>(GList);
		
		public GroupPanel(Window window) {
			this.setBackground(Color.WHITE);
			this.setLayout(new BorderLayout());
			for(compositePattern.Group g: Application.currentuser.getGroupsJoined()) {
				GList.addElement(" " + g.getName());
			}	
			for(compositePattern.Group g: Application.currentuser.getGroupsRepresented()) {
				GList.addElement(" " + g.getName());
			}	
			
			
			list.addListSelectionListener(new GroupListener(list, window));
			JScrollPane scrollbar= new JScrollPane(list);
			scrollbar.setPreferredSize(new Dimension(150,225));
			list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
			this.add(scrollbar, BorderLayout.NORTH);	
			
		    this.setPreferredSize(new Dimension(150, 250));	
		    this.setVisible(true); 
		}
}
		
class ProjectPanel extends JPanel {

	private static final long serialVersionUID = 1L;
			
	DefaultListModel<String> PList = new DefaultListModel<String>();				
	JList<String> list= new JList<String>(PList);

			
	public ProjectPanel(Window window) {
		this.setBackground(Color.WHITE);
		this.setLayout(new BorderLayout());
		for(project.Project p: Application.currentuser.getProjectsSubscribed()) {
			PList.addElement(" " + p.getName());
		}
		list.addListSelectionListener(new ProjectListener(list, window));
		JScrollPane scrollbar= new JScrollPane(list);
		scrollbar.setPreferredSize(new Dimension(150,225));
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		this.add(scrollbar, BorderLayout.NORTH);	
		
	    this.setPreferredSize(new Dimension(150, 250));	
	    this.setVisible(true); 
	}
	
}
		

class Notification implements ActionListener {
	
	private Component generalpanel;
	private JButton not;
	private ImageIcon notIcon;
	private ImageIcon noNotIcon;
	

	public Notification(Component whereToDisplayMessage, JButton not, ImageIcon notIcon, ImageIcon noNotIcon) {

		this.generalpanel = whereToDisplayMessage;
		this.not = not;
		this.notIcon = notIcon;
		this.noNotIcon = noNotIcon;

	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		
		if(Application.currentuser.getReadNotification() == true) {
			
		    this.not.setIcon(notIcon);
			not.setVisible(true);
			new UsersNotifications();
		}
		else {
		    this.not.setIcon(noNotIcon);
			not.setVisible(true);
			JOptionPane.showMessageDialog(generalpanel, "You don't have new notifications");	
		}
		
	}

		
		
}    

class GroupListener implements ListSelectionListener {
	Window window;
	JList<String> list;
	public GroupListener(JList<String> list, Window window) {
		this.window = window;
		this.list = list;
	}

	public void valueChanged(ListSelectionEvent e) {
		String[] splitter = list.getSelectedValue().split(" ");
		String projectname = splitter[1];
		Group myProj = Group.getGroup(projectname);
		if(myProj == null) {
			return;
		}
		window.showPanel(new GroupScreen(myProj, window));
	}
}




class ProjectListener implements ListSelectionListener {
	JList<String> list;
	Window window;
	public ProjectListener(JList<String> list, Window window) {
		super();
		this.list = list;
		this.window = window;
	}

	@Override
	public void valueChanged(ListSelectionEvent e) {
		String[] splitter = list.getSelectedValue().split(" ");
		String projectname = splitter[1];
		Project myProj = Project.getProject(projectname);
		if(myProj == null) {
			return;
		}
		window.showPanel(new ProjectScreen(window, myProj));
	}
}

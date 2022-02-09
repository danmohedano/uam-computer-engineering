package gui.user;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import compositePattern.RegisteredCitizen;
import exception.projectExceptions.InvalidThresholdProjectException;
import gui.window.ICard;
import gui.window.Window;
import project.Project;
import project.Status;;

/**
 * The GUI for the Admin's Profile
 * @author Silvia Sope�a Niecko silvia.sopenna@estudiante.uam.es
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 * 
 */

public class AdminsProfile extends JPanel implements ICard {

	private static final long serialVersionUID = 1L;
	
	private SouthLayoutAdmin south; 
	private int sizex = 650;
	private int sizey = 210;
	Window window;
	public AdminsProfile(Window window) {
		south =new SouthLayoutAdmin(window);
		this.window = window;
		SpringLayout layout = new SpringLayout();
		this.setLayout(layout);
		this.setBackground(Color.WHITE);
		
		JLabel header = new JLabel("Administrator's profile"); 
		Font f = new Font(header.getFont().getFontName(), Font.BOLD, 24);
		header.setFont(f);
		
		layout.putConstraint(SpringLayout.NORTH, header, 5, SpringLayout.NORTH, this);
		layout.putConstraint(SpringLayout.WEST, header, 5, SpringLayout.WEST, this);
		this.add(header);
		
		layout.putConstraint(SpringLayout.NORTH, south, 5, SpringLayout.SOUTH, header);
		layout.putConstraint(SpringLayout.WEST, south, 5, SpringLayout.WEST, this);
		this.add(south);
		
		this.setPreferredSize(new Dimension(sizex, sizey));

	}
	


	@Override
	public int definedSizeY() {
		return sizey;
	}


	@Override
	public int definedSizeX() {
		return sizex;
	}


	@Override
	public JPanel getPanel() {
		return this;
	}
	
	
}



class SouthLayoutAdmin extends JPanel {
	
	private static final long serialVersionUID = 1L;

	private AL right;
	private AP left;
	private BannedUsers banned;
	private NewUsers newuser;
	public SouthLayoutAdmin(Window window) {
		right  = new AL(window);
		left  = new AP(window);
		banned  = new BannedUsers(window);
		newuser = new NewUsers(window);
		SpringLayout layout = new SpringLayout();
		this.setLayout(layout);
		this.setBackground(Color.WHITE);

		right.setBorder(BorderFactory.createTitledBorder("<html><b>New Projects</b></html>"));
		banned.setBorder(BorderFactory.createTitledBorder("<html><b>Banned Users</b></html>"));
		newuser.setBorder(BorderFactory.createTitledBorder("<html><b>New Users</b></html>"));

		layout.putConstraint(SpringLayout.WEST, left, 5, SpringLayout.WEST, this);
	    layout.putConstraint(SpringLayout.NORTH, left, 5, SpringLayout.NORTH, this);
	    this.add(left);
	    
	    layout.putConstraint(SpringLayout.WEST, right, 5, SpringLayout.EAST, left);
	    layout.putConstraint(SpringLayout.NORTH, right, 0, SpringLayout.NORTH, left);
	    this.add(right);
	    
	    layout.putConstraint(SpringLayout.WEST, banned, 5, SpringLayout.EAST, right);
	    layout.putConstraint(SpringLayout.NORTH, banned, 0, SpringLayout.NORTH, right);
	    this.add(banned);
	    
	    layout.putConstraint(SpringLayout.WEST, newuser, 5, SpringLayout.EAST, banned);
	    layout.putConstraint(SpringLayout.NORTH, newuser, 0, SpringLayout.NORTH, banned);
	    this.add(newuser);
	    

		
	    this.setPreferredSize(new Dimension(650, 170));	
	    this.setVisible(true); 
	}
	

}

class AL extends JPanel {

	private static final long serialVersionUID = 1L;
			
	DefaultListModel<String> PList = new DefaultListModel<String>();				
	JList<String> list= new JList<String>(PList);
	private int sizex = 150;
	private int sizey = 135;
			
	public AL(Window window) {

		for(Project p: Project.projectByStatus(Status.CREATED)) {
			PList.addElement(p.getName());
		}	

		this.setLayout(new BorderLayout());
		this.setBackground(Color.WHITE);
		JScrollPane scrollbar= new JScrollPane(list);
		scrollbar.setPreferredSize(new Dimension(sizex, sizey));
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		this.add(scrollbar, BorderLayout.NORTH);	
		list.addListSelectionListener(new AcceptReject(this.list, window));
		this.setPreferredSize(new Dimension(sizex, sizey+25));	
		this.setVisible(true); 
	}
	
}

class BannedUsers extends JPanel {

	private static final long serialVersionUID = 1L;
			
	DefaultListModel<String> PList = new DefaultListModel<String>();				
	JList<String> list= new JList<String>(PList);
	private int sizex = 150;
	private int sizey = 135;
			
	public BannedUsers(Window window) {
		
		for(RegisteredCitizen p: RegisteredCitizen.getAllCitizens()) {
			if(p.getBan() == true)
				PList.addElement(p.getName());
		}	
		this.setLayout(new BorderLayout());
		this.setBackground(Color.WHITE);
		JScrollPane scrollbar= new JScrollPane(list);
		scrollbar.setPreferredSize(new Dimension(sizex, sizey));
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		this.add(scrollbar, BorderLayout.NORTH);	
		list.addListSelectionListener(new UnBanListener(this.list, window));
		this.setPreferredSize(new Dimension(sizex, sizey+25));	
		this.setVisible(true); 
	}
	
}

class NewUsers extends JPanel {

	private static final long serialVersionUID = 1L;
			
	DefaultListModel<String> PList = new DefaultListModel<String>();				
	JList<String> list= new JList<String>(PList);
	private int sizex = 150;
	private int sizey = 135;
			
	public NewUsers(Window window) {
		
		for(RegisteredCitizen p: RegisteredCitizen.getNewCitizens()) {
				PList.addElement(p.getName());
		}	
		this.setLayout(new BorderLayout());
		this.setBackground(Color.WHITE);
		JScrollPane scrollbar= new JScrollPane(list);
		scrollbar.setPreferredSize(new Dimension(sizex, sizey));
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		this.add(scrollbar, BorderLayout.NORTH);	
		list.addListSelectionListener(new AcceptUsers(this.list, window));
		this.setPreferredSize(new Dimension(sizex, sizey+25));	
		this.setVisible(true); 
	}
	
}



class AP extends JPanel {
	
	private static final long serialVersionUID = 1L;
	private JButton ban = new JButton(new ImageIcon("files/banicon.png"));
	private JComboBox<String> combobox;
	private List<String> users = new ArrayList<String>();
	 
	private JLabel threshold;
	JTextField newthreshold = new JTextField("", 10);
	JButton newthresholdbutton = new JButton("Set");
	
	
	public AP(Window window) {
	    SpringLayout layout = new SpringLayout();	
	    ban.setPreferredSize(new Dimension(30, 30));
	    this.setLayout(layout); 
		this.setBackground(Color.WHITE);
	    for(RegisteredCitizen x: RegisteredCitizen.getAllCitizens()) {
	    	users.add(x.getName());
	    }
	    
	    threshold  = new JLabel("Threshold: " + Project.getThreshold());
	    Font f = new Font(threshold.getFont().getFontName(), Font.BOLD, 12);
	    threshold.setFont(f);
	    newthresholdbutton.addActionListener(new setThreshold(window, newthreshold));
	    String i[] = {};
	    this.combobox = new JComboBox<String>(users.toArray(i));
	    combobox.setPreferredSize(new Dimension(100, 30));
	    newthresholdbutton.setPreferredSize(new Dimension(50, 30));
	    newthreshold.setPreferredSize(new Dimension(30, 30));

	    layout.putConstraint(SpringLayout.WEST, combobox, 5, SpringLayout.WEST, this);
	    layout.putConstraint(SpringLayout.NORTH, combobox, 5, SpringLayout.NORTH, this);
	    layout.putConstraint(SpringLayout.WEST, ban, 5, SpringLayout.EAST, combobox);
	    layout.putConstraint(SpringLayout.NORTH, ban, 0, SpringLayout.NORTH, combobox);
		this.add(combobox);
	    layout.putConstraint(SpringLayout.NORTH, threshold, 5, SpringLayout.SOUTH, combobox);
		this.add(ban);
	    layout.putConstraint(SpringLayout.WEST, threshold, 5, SpringLayout.WEST, this);
		this.add(threshold);
		layout.putConstraint(SpringLayout.WEST, newthreshold, 0, SpringLayout.WEST, threshold);
	    layout.putConstraint(SpringLayout.NORTH, newthreshold, 5, SpringLayout.SOUTH, threshold);
		this.add(newthreshold);
		layout.putConstraint(SpringLayout.WEST, newthresholdbutton, 5, SpringLayout.EAST, newthreshold);
	    layout.putConstraint(SpringLayout.NORTH, newthresholdbutton, 5, SpringLayout.SOUTH, threshold);
		this.add(newthresholdbutton);
		
		ban.addActionListener(new BanUser(this, combobox, window));
		
	    this.setPreferredSize(new Dimension(145, 100));	
	    this.setVisible(true); 
	}
}
	
	
	

			
class AcceptReject implements ListSelectionListener{
	
	private JList<String> list;
	private Window window;
	public AcceptReject(JList<String> list, Window window) {
		this.list = list;
		this.window = window;
	}
	
	@Override
	public void valueChanged(ListSelectionEvent e) {
		
		if(!e.getValueIsAdjusting()) {
			new AdminAcceptReject(window, list.getSelectedValue());
		}
	}
	
}

class BanUser implements ActionListener {
	
	private JComboBox<String> combobox;
	Window window;
	public BanUser(Component whereToDisplayMessage, JComboBox<String> combobox, Window window) {
		this.combobox = combobox;
		this.window = window;
	}
	
	public void actionPerformed(ActionEvent e) {
		String x = (String) combobox.getSelectedItem();
		if(x== null) return;
		RegisteredCitizen.getCitizenByName(x).banUser();
		window.showPanel(new AdminsProfile(window));
		return;	
	}
	
}


class UnBanListener implements ListSelectionListener{
	
	private JList<String> list;
	Window window;
	public UnBanListener(JList<String> list, Window window) {
		this.list = list;
		this.window = window;
	}
	
	@Override
	public void valueChanged(ListSelectionEvent e) {
		
		if(!e.getValueIsAdjusting()) {
			String[] splitter = list.getSelectedValue().split(" ");
			String name  = splitter[0];
			RegisteredCitizen unban = RegisteredCitizen.getCitizenByName(name);
			if(unban != null) {
				unban.setBan(false);
				window.showPanel(new AdminsProfile(window));
				
			}
			else {
				return;
			}
		}
	}
	
}


class AcceptUsers implements ListSelectionListener{
	
	private JList<String> list;
	Window window;
	public AcceptUsers(JList<String> list, Window window) {
		this.list = list;
		this.window = window;
	}
	
	@Override
	public void valueChanged(ListSelectionEvent e) {
		
		if(!e.getValueIsAdjusting()) {
			String name  = list.getSelectedValue();
			RegisteredCitizen target = null;
			for(RegisteredCitizen myCit: RegisteredCitizen.getNewCitizens()) {
				if(myCit.getName().equals(name)) {
					target = myCit;
					break;
				}
			}
			if(target != null) {
				if (JOptionPane.showConfirmDialog(window, "Accept user?\nName: " + target.getName(), "accept user", JOptionPane.OK_CANCEL_OPTION) != 0) {
					RegisteredCitizen.getAllCitizens().remove(target);
				}
				RegisteredCitizen.removeNewCitizens(target);
				window.showPanel(new AdminsProfile(window));
				return;				
			}
			window.showPanel(new AdminsProfile(window));
			return;
		}
	}
	
}



class setThreshold implements ActionListener{
	JTextField quantity;
	Window window;
	public setThreshold(Window window, JTextField quantity) {
		this.window = window;
		this.quantity = quantity;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		int i;
		System.out.println(quantity.getText());
		try{ 
			i = Integer.parseInt(quantity.getText());
		}
		catch(NumberFormatException e1) {
			JOptionPane.showMessageDialog(window, e1);
			JOptionPane.showMessageDialog(window, "Please select a valid threshold");
			return;
		}
		
		try {
			Project.setThreshold(i);
		} catch (InvalidThresholdProjectException e1) {
			JOptionPane.showMessageDialog(window, "Please select a positive threshold");
			return;
		}
		window.showPanel(new AdminsProfile(window));
			
		
	}

	
	
}


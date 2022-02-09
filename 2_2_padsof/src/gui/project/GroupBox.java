/**
 * 
 */
package gui.project;

import java.awt.Color;
import java.awt.Dimension;
import java.util.ArrayList;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.TitledBorder;

import application.Application;
import compositePattern.Group;

/**
 * Class to represent a Combo Box with the groups represented by the user
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class GroupBox extends JPanel{
	private JComboBox<String> box;
	private int sizex = 41; //Base length of border string
	private int sizey = 75;
	
	public GroupBox() {
		this.setBackground(Color.WHITE);
		//Get list of represented groups by the current user to add to the box
		List<String> groupNames = new ArrayList<>();
		groupNames.add("None");
		for (Group x : Application.currentuser.getGroupsRepresented()) {
			groupNames.add(x.getName());
			if (x.getName().length() > sizex) sizex = x.getName().length(); //Adapt size to group names
		}
		String s[] = new String[groupNames.size()];
		box = new JComboBox<String>(groupNames.toArray(s));
		
		sizex = sizex*120/14; //Fix size
		
		this.setBorder(BorderFactory.createTitledBorder(null, "Associate to one of your groups:", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));
		this.add(box);
		
		this.setPreferredSize(new Dimension(sizex, sizey));
		this.setVisible(true);
	}
	
	/**
	 * returns the sizex of the panel
	 * @return size x
	 */
	public int definedSizeX() {
		return this.sizex;
	}
	/**
	 * returns the sizey of the panel
	 * @return size y
	 */
	public int definedSizeY() {
		return this.sizey;
	}
	
	/**
	 * returns the combo box to access the information
	 * @return size x
	 */
	public JComboBox<String> getBox(){
		return this.box;
	}
}

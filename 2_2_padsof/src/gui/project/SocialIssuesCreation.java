/**
 * 
 */
package gui.project;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.border.TitledBorder;

import application.Application;
import compositePattern.Group;
import gui.window.ICard;
import gui.window.Window;
import project.SocialIssuesProject;

/**
 * Main panel to create a social issues project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class SocialIssuesCreation extends JPanel implements ICard{
	private Window window;
	private JLabel title = new JLabel("Social Issues", JLabel.CENTER);
	private JTextField name = new JTextField("", 20);;
	private JRadioButton jrbs[] = {new JRadioButton("National"), new JRadioButton("International")};
	private ButtonGroup bg = new ButtonGroup();
	private JButton confirm = new JButton("Confirm");
	
	private String projectName;
	private String description;
	private double budget;
	private Group group;
	
	private int sizex = 850;
	private int sizey = 650;
	
	public SocialIssuesCreation(Window window, String projectName, String description, double budget, Group group) {
		this.setBackground(Color.WHITE);
		this.window = window;
		this.projectName = projectName;
		this.description = description;
		this.budget = budget;
		this.group = group;
		JPanel firstSection = new JPanel();
		JPanel secondSection = new JPanel();
		
		//Setup first section (social group name)
		firstSection.setLayout(new BorderLayout());
		firstSection.setBorder(BorderFactory.createTitledBorder(null, "Provide the social group name affected:", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));

		firstSection.add(this.name, BorderLayout.CENTER);
		firstSection.setVisible(true);
		firstSection.setPreferredSize(new Dimension(400, 100));
		
		
		//Setup second section (aim)
		secondSection.setLayout(new BorderLayout());
		secondSection.setBorder(BorderFactory.createTitledBorder(null, "Select the aim of the project:", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));
		for (JRadioButton jb : jrbs) {
			bg.add(jb);
			jb.setBackground(Color.WHITE);
		}
		secondSection.add(jrbs[0], BorderLayout.NORTH);
		secondSection.add(jrbs[1], BorderLayout.SOUTH);
		secondSection.setVisible(true);
		secondSection.setPreferredSize(new Dimension(400, 100));
		
		//Setup center area
		JPanel center = new JPanel();
		center.setLayout(new GridBagLayout());
		GridBagConstraints gbc = new GridBagConstraints();
		gbc.gridx = 0;
		gbc.gridy = 0;
		center.add(firstSection, gbc);
		gbc.gridx = 0;
		gbc.gridy = 1;
		center.add(secondSection, gbc);
		center.setVisible(true);
		center.setPreferredSize(new Dimension(800, 400));
		
		center.setBackground(Color.WHITE);
		firstSection.setBackground(Color.WHITE);
		secondSection.setBackground(Color.WHITE);
		//Setup global panel
		this.setLayout(new BorderLayout());
		this.title.setFont(new Font(super.getFont().getFontName(), Font.BOLD, 24));
		confirm.addActionListener(new ConfirmCreationSI(this.window, this, this.name, this.jrbs, this.projectName, this.description, this.budget, this.group));
		this.add(title, BorderLayout.NORTH);
		this.add(center, BorderLayout.CENTER);
		this.add(confirm, BorderLayout.SOUTH);
		this.setPreferredSize(new Dimension(this.sizex, this.sizey));
		
	}
	
	public int definedSizeX() { return this.sizex;}
	
	public int definedSizeY() { return this.sizey;}
	
	public JPanel getPanel() {return this;}
}

class ConfirmCreationSI implements ActionListener{
	private Window generalPanel;
	private Component window;
	private JTextField groupName;
	private JRadioButton[] aim;
	private String name;
	private String description;
	private double budget;
	private Group group;
	
	public ConfirmCreationSI(Window generalPanel, Component window, JTextField groupName, JRadioButton aim[], String name, String description, double budget, Group group) {
		this.generalPanel = generalPanel;
		this.window = window;
		this.groupName = groupName;
		this.aim = aim;
		this.name = name;
		this.description = description;
		this.budget = budget;
		this.group = group;
	}
	
	@Override
	public void actionPerformed(ActionEvent arg0) {
		if (groupName.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(window, "Must provide a name for the affected social group.");
			return;
		}

		if (!aim[0].isSelected() && !aim[1].isSelected()) {
			JOptionPane.showMessageDialog(window, "Must select an aim for the project.");
			return;
		}
		
		boolean a;
		if (aim[0].isSelected()) a = false;
		else a = true;
		
		SocialIssuesProject x;
		
		try {
			if (group == null)
				x = new SocialIssuesProject(name, description, budget, Application.currentuser, groupName.getText(), a);
			else x = new SocialIssuesProject(name, description, budget, Application.currentuser, group, groupName.getText(), a);
		} catch (Exception e1) {
			JOptionPane.showMessageDialog(window, e1);
			return;
		}
		
		ICard card = new ProjectScreen(generalPanel, x);
		generalPanel.showPanel(card);
		
	}
	
}
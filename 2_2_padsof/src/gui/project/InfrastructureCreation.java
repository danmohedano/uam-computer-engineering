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
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import project.InfrastructureProject;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import application.Application;
import compositePattern.Group;
import gui.window.ICard;
import gui.window.Window;

/**
 * Main panel for the creation of an infrastructure project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class InfrastructureCreation extends JPanel implements ICard{
	private Window window;
	private JLabel title = new JLabel("Infrastructure", JLabel.CENTER);
	private JTextField filename = new JTextField("", 20);
	private DefaultListModel<String> baseList = new DefaultListModel<String>();
	private JList<String> neighborhoods = new JList<String>(baseList);
	private DefaultListModel<String> baseSelected = new DefaultListModel<String>();
	private JList<String> selected = new JList<String>(baseSelected);
	private JButton confirm = new JButton("Confirm");
	
	private String name;
	private String description;
	private double budget;
	private Group group;
	
	private int sizex = 850;
	private int sizey = 650;
	
	public InfrastructureCreation(Window window, String name, String description, double budget, Group group) {
		this.setBackground(Color.WHITE);
		this.window = window;
		this.name = name;
		this.description = description;
		this.budget = budget;
		this.group = group;
		//Setup list of neighborhoods
		try {
			InfrastructureProject.readDistricts();
		} catch (IOException e) {
			System.out.println("Error reading districts.\n");
			e.printStackTrace();
		}

		baseList.addAll(InfrastructureProject.districts);
		this.neighborhoods.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		this.neighborhoods.setLayoutOrientation(JList.VERTICAL);
		this.selected.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		this.selected.setLayoutOrientation(JList.VERTICAL);
		
		this.neighborhoods.addListSelectionListener(new NeighborhoodSelection(this.baseList, this.baseSelected, this.neighborhoods));
		this.selected.addListSelectionListener(new NeighborhoodSelection(this.baseSelected, this.baseList, this.selected));
		
		JPanel firstSection = new JPanel();
		JPanel secondSection = new JPanel();
		JPanel thirdSection = new JPanel();
		
		//Setup first section (filename)
		firstSection.setLayout(new BorderLayout());
		firstSection.setBorder(BorderFactory.createTitledBorder(null, "Upload a graphical scheme (filename):", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));

		firstSection.add(this.filename, BorderLayout.CENTER);
		firstSection.setVisible(true);
		firstSection.setPreferredSize(new Dimension(400, 100));
		
		//Setup second section (districts)
		JScrollPane scroll1 = new JScrollPane(this.neighborhoods);
		secondSection.setLayout(new BorderLayout());
		secondSection.setBorder(BorderFactory.createTitledBorder(null, "List of neighborhoods available:", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));
		
		secondSection.add(scroll1, BorderLayout.CENTER);
		secondSection.setVisible(true);
		secondSection.setPreferredSize(new Dimension(400,300));
		
		//Setup third section (list of districts selected)
		JScrollPane scroll2 = new JScrollPane(this.selected);
		thirdSection.setLayout(new BorderLayout());
		thirdSection.setBorder(BorderFactory.createTitledBorder(null, "List of neighborhoods affected:", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));
		
		thirdSection.add(scroll2, BorderLayout.CENTER);
		thirdSection.setVisible(true);
		thirdSection.setPreferredSize(new Dimension(400, 400));
		
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
		gbc.gridx = 1;
		gbc.gridy = 0;
		gbc.gridheight = 2;
		gbc.fill = GridBagConstraints.VERTICAL;
		center.add(thirdSection, gbc);
		center.setPreferredSize(new Dimension(800,400));
		
		//Setup global panel
		this.setLayout(new BorderLayout());
		this.title.setFont(new Font(super.getFont().getFontName(), Font.BOLD, 24));
		confirm.addActionListener(new ConfirmCreationI(this.window, this, this.filename, this.selected, this.name, this.description, this.budget, this.group));
		center.setBackground(Color.WHITE);
		firstSection.setBackground(Color.WHITE);
		secondSection.setBackground(Color.WHITE);
		thirdSection.setBackground(Color.WHITE);
		this.add(title, BorderLayout.NORTH);
		this.add(center, BorderLayout.CENTER);
		this.add(confirm, BorderLayout.SOUTH);
		
		this.setPreferredSize(new Dimension(this.sizex, this.sizey));
	}
	
	/**
	 * returns the sizex of the panel
	 * @return size x
	 */
	public int definedSizeX() {return this.sizex;}
	/**
	 * returns the sizey of the panel
	 * @return size y
	 */
	public int definedSizeY() {return this.sizey;}
	/**
	 * returns the panel
	 * @return panel
	 */
	public JPanel getPanel() {return this;}
}

/**
 * Class to represent the neighborhood selection panel
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class NeighborhoodSelection implements ListSelectionListener{
	private DefaultListModel<String> to;
	private DefaultListModel<String> from;
	private JList<String> subject;
	
	public NeighborhoodSelection(DefaultListModel<String> to, DefaultListModel<String> from, JList<String> subject) {
		this.to = to;
		this.from = from;
		this.subject = subject;
	}
	
	@Override
	public void valueChanged(ListSelectionEvent e) {
		if (!e.getValueIsAdjusting()) {
			String selected = subject.getSelectedValue();
			to.removeElement(selected);
			from.addElement(selected);
		}
	}
	
}

/**
 * Listener to confirm the creation of an infrastructure project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class ConfirmCreationI implements ActionListener{
	private Window generalPanel;
	private Component window;
	private JTextField filename;
	private JList<String> districts;
	private String name;
	private String description;
	private double budget;
	private Group group;
	
	public ConfirmCreationI(Window generalPanel, Component window, JTextField filename, JList<String> districts, String name, String description, double budget, Group group) {
		this.generalPanel = generalPanel;
		this.window = window;
		this.filename = filename;
		this.districts = districts;
		this.name = name;
		this.description = description;
		this.budget = budget;
		this.group = group;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if (filename.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(window, "Must provide a filename for the graphical scheme.");
			return;
		}
		List<String> ds = new ArrayList<>();
		for (int i = 0; i < districts.getModel().getSize(); i++) {
			ds.add(districts.getModel().getElementAt(i));
		}
		
		try {
			@SuppressWarnings("unused")
			BufferedImage myPicture = ImageIO.read(new File(this.filename.getText()));
		} catch (IOException e2) {
			JOptionPane.showMessageDialog(window, "Must provide a valid file for the graphical scheme.");
			return;
		}
		InfrastructureProject x;
		
		try {
			if (group == null)
				x = new InfrastructureProject(name, description, budget, Application.currentuser, filename.getText(), ds);
			else x = new InfrastructureProject(name, description, budget, Application.currentuser, group, filename.getText(), ds);
		} catch (Exception e1) {
			JOptionPane.showMessageDialog(window, e1);
			e1.printStackTrace();
			return;
		}
		
		ICard card = new ProjectScreen(generalPanel, x);
		generalPanel.showPanel(card);
	}
}

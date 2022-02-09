package gui.group;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.DecimalFormat;
import java.util.ArrayList;

import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeSelectionModel;

import application.Application;
import compositePattern.Group;
import exception.groupExceptions.GroupContainsUserException;
import exception.groupExceptions.MemberNotContainedException;
import exception.groupExceptions.RemoveRepresentativeException;
import gui.project.ProjectScreen;
import gui.window.ICard;
import gui.window.Window;
import project.Project;

/**
 * Group creation
 * 
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class GroupScreen extends JPanel implements ICard {
	private TitlePanel header;
	private SubGroupPanel tree;
	private ProjectsSupportedPanel projectspanel;
	SimilarityPanel similarityreport; 
	private JButton joinBut = new JButton();
	private JButton leaveBut = new JButton();

	JPanel groupscreen = this;

	private int sizex = 1000;
	private int sizey = 1000;
	Group group;

	public int definedSizeX() {
		return this.sizex;
	}

	public int definedSizeY() {
		return this.sizey;
	}

	public GroupScreen(Group group, Window window) {
		this.setBackground(Color.WHITE);

		joinBut.setIcon(new ImageIcon("files/join30.png"));
		leaveBut.setIcon(new ImageIcon("files/leave30.png"));
		this.setPreferredSize(new Dimension(sizex, sizey));
		this.group = group;
		similarityreport = new SimilarityPanel(window, group);
		header = new TitlePanel(group);
		tree = new SubGroupPanel(window, group);
		projectspanel = new ProjectsSupportedPanel(window, group);
		Container cp = this;
		SpringLayout layout = new SpringLayout();
		cp.setLayout(layout);

		layout.putConstraint(SpringLayout.NORTH, header, 5, SpringLayout.NORTH, this);
		layout.putConstraint(SpringLayout.WEST, header, 5, SpringLayout.WEST, this);
		this.add(header);

		layout.putConstraint(SpringLayout.NORTH, tree, 5, SpringLayout.SOUTH, header);
		layout.putConstraint(SpringLayout.WEST, tree, 5, SpringLayout.WEST, this);
		this.add(tree);
		layout.putConstraint(SpringLayout.NORTH, projectspanel, -6, SpringLayout.NORTH, tree);
		layout.putConstraint(SpringLayout.WEST, projectspanel, 5, SpringLayout.EAST, tree);
		this.add(projectspanel);
		layout.putConstraint(SpringLayout.NORTH, similarityreport, -14, SpringLayout.NORTH, projectspanel);
		layout.putConstraint(SpringLayout.WEST, similarityreport, 5, SpringLayout.EAST, projectspanel);
		this.add(similarityreport);

		
		layout.putConstraint(SpringLayout.SOUTH, joinBut, -5, SpringLayout.NORTH, projectspanel);
		layout.putConstraint(SpringLayout.WEST, joinBut, 65, SpringLayout.WEST, projectspanel);
		this.add(joinBut);
		layout.putConstraint(SpringLayout.SOUTH, leaveBut, -5, SpringLayout.NORTH, projectspanel);
		layout.putConstraint(SpringLayout.WEST, leaveBut, 65, SpringLayout.WEST, projectspanel);
		this.add(leaveBut);

		if (group.RegisteredCitizenDirectlyContained(Application.currentuser) == false)
			leaveBut.setVisible(false);
		else
			joinBut.setVisible(false);
		joinBut.addActionListener(new JoinListener(this.group, this, joinBut, leaveBut));
		leaveBut.addActionListener(new LeaveListener(this.group, this, joinBut, leaveBut));

		

		sizex = tree.definedSizeX() + projectspanel.definedSizeX() +similarityreport.definedSizeX() + 35;
		sizey = header.definedSizeY() + tree.definedSizeY() +15;
		this.setPreferredSize(new Dimension(sizex, sizey)); // importante: tamaño preferido de este panel
		this.setVisible(true);
	}

	@Override
	public JPanel getPanel() {
		return this;
	}

}

@SuppressWarnings("serial")
class TitlePanel extends JPanel {
	private JLabel title;
	private JLabel subtitle;
	private int sizex;
	private int sizey = 50;

	public TitlePanel(Group group) {
		this.setBackground(Color.WHITE);
		this.setLayout(new BorderLayout()); // muy flexible, pero de bajo nivel.
		sizex = 225;

		this.title = new JLabel(group.getName());
		Font f = new Font(super.getFont().getFontName(), Font.BOLD, 24);
		title.setFont(f);
		this.add(title, BorderLayout.NORTH);

		

		this.subtitle = new JLabel("Represented by " + group.getRepresentative().getName());
		subtitle.setFont(new Font(super.getFont().getFontName(), Font.ITALIC, 15));
		this.add(subtitle, BorderLayout.SOUTH);

		this.setPreferredSize(new Dimension(sizex, sizey)); // importante: tamaño preferido de este panel
		this.setVisible(true);
	}

	public int definedSizeY() {
		return sizey;
	}

	public int definedSizeX() {
		return sizex;
	}

}

@SuppressWarnings("serial")
class SubGroupPanel extends JPanel {
	Window window;
	private int sizex = 200;
	private int sizey = 390;
	DefaultMutableTreeNode root;
	final JTree tree;

	public SubGroupPanel(Window window, Group group) {
		this.setBackground(Color.WHITE);

		this.window = window;
		this.setLayout(new BorderLayout()); // muy flexible, pero de bajo nivel.
		if(group.getFather() != null) {
			root = new DefaultMutableTreeNode(group.getFather().getName());
			root.add(new DefaultMutableTreeNode(group.getName()));
		}
		else root = new DefaultMutableTreeNode(group.getName());
		
		tree = new JTree(root);
		tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);

		for (Group myGroup : group.getChildren()) {
			generateTree(myGroup, root);
		}

		JScrollPane scrollbar = new JScrollPane(tree);
		scrollbar.setPreferredSize(new Dimension(sizex, sizey));
		tree.addTreeSelectionListener(new TreeButtonListener(window, tree));
		expandAllNodes(tree);
		
		this.add(scrollbar, BorderLayout.NORTH);
		this.setPreferredSize(new Dimension(sizex, sizey)); // importante: tamaño preferido de este panel
		this.setVisible(true);
	}

	public int definedSizeY() {
		return sizey;
	}

	public int definedSizeX() {
		return sizex;
	}

	private void generateTree(Group group, DefaultMutableTreeNode root) {
		if (group.getChildren().isEmpty() == true) {
			root.add(new DefaultMutableTreeNode(group.getName()));
			return;
		}

		DefaultMutableTreeNode folder = new DefaultMutableTreeNode(group.getName());
		for (Group myGroup : group.getChildren()) {
			generateTree(myGroup, folder);
		}
		root.add(folder);
	}

	private void expandAllNodes(JTree tree) {
		int j = tree.getRowCount();
		int i = 0;
		while (i < j) {
			tree.expandRow(i);
			i += 1;
			j = tree.getRowCount();
		}
	}

}

@SuppressWarnings("serial")
class ProjectsSupportedPanel extends JPanel {
	Window window;
	private JList<String> listaCreated;
	private JList<String> listaSup;
	private int sizex = 200;
	private int sizey = 390 + 8;

	public ProjectsSupportedPanel(Window window, Group group) {
		this.setBackground(Color.WHITE);

		this.window = window;
		this.setLayout(new BorderLayout()); // muy flexible, pero de bajo nivel.
		ArrayList<String> stringCreated = new ArrayList<String>();
		for (Project myProj : group.getProjectsCreated()) {
			stringCreated.add(" " + myProj.getName());
		}
		ArrayList<String> stringSup = new ArrayList<String>();
		for (Project myProj : group.getProjectsSupported()) {
			stringSup.add(" " + myProj.getName());
		}

		DefaultListModel<String> listModelCreat = new DefaultListModel<String>();
		for (int i = 0; i < stringCreated.size(); i++)
			listModelCreat.addElement(stringCreated.get(i));

		DefaultListModel<String> listModelSup = new DefaultListModel<String>();
		for (int i = 0; i < stringSup.size(); i++)
			listModelSup.addElement(stringSup.get(i));

		listaCreated = new JList<String>(listModelCreat);
		listaSup = new JList<String>(listModelSup);
		listaSup.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		listaCreated.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		listaSup.addListSelectionListener(new ListButtonListener(listaSup, window));
		listaCreated.addListSelectionListener(new ListButtonListener(listaCreated, window));

		JScrollPane scrollbar = new JScrollPane(listaSup);
		JScrollPane scrollbar2 = new JScrollPane(listaCreated);
		scrollbar.setPreferredSize(new Dimension(sizex, sizey / 2 - 10));
		scrollbar2.setPreferredSize(new Dimension(sizex, sizey / 2 - 10));
		scrollbar.setBorder(BorderFactory.createTitledBorder("<html><b>Supported Projects</b></html>"));
		scrollbar2.setBorder(BorderFactory.createTitledBorder("<html><b>Created Projects</b></html>"));
		scrollbar.setBackground(Color.WHITE);
		scrollbar2.setBackground(Color.WHITE);

		this.add(scrollbar, BorderLayout.NORTH);
		this.add(scrollbar2, BorderLayout.CENTER);
		this.setPreferredSize(new Dimension(sizex, sizey)); // importante: tamaño preferido de este panel
		this.setVisible(true);
	}

	public int definedSizeY() {
		return sizey;
	}

	public int definedSizeX() {
		return sizex;
	}

}

@SuppressWarnings("serial")
class SimilarityPanel extends JPanel {
	Window window;
	int sizex = 200;
	int sizey = 410;
	JButton confirmbutton = new JButton("<html>no group selected<br></html>");
	public SimilarityPanel(Window window, Group group) {
		this.setBackground(Color.WHITE);
		this.window = window;
		this.setLayout(new BorderLayout());
		JPanel searchbox = new JPanel();
		searchbox.setBackground(Color.WHITE);

		JTextField field = new JTextField(14);
		JButton clicksearch = new JButton();
		clicksearch.setIcon(new ImageIcon("files/search20.gif"));
		clicksearch.setPreferredSize(new Dimension(25, 20));
		
		searchbox.setLayout(new GridBagLayout());
		GridBagConstraints constraints = new GridBagConstraints();
		constraints.gridx = 0; // El área de texto empieza en la columna cero.
		constraints.gridy = 0; // El área de texto empieza en la fila cero
		constraints.gridwidth = 2; // El área de texto ocupa dos columnas.
		constraints.gridheight = 2; // El área de texto ocupa 2 filas.
		searchbox.add(field, constraints);
		GridBagConstraints constraints2 = new GridBagConstraints();
		constraints2.gridx = 2; // El área de texto empieza en la columna cero.
		constraints2.gridy = 0; // El área de texto empieza en la fila cero
		constraints2.gridwidth = 2; // El área de texto ocupa dos columnas.
		constraints2.gridheight = 2; // El área de texto ocupa 2 filas.
		searchbox.add(clicksearch, constraints2);
		
		this.add(searchbox, BorderLayout.NORTH);
		
		DefaultListModel<String> results = new DefaultListModel<String>();
		clicksearch.addActionListener(new SearchGroupListener(results,field));

		JList<String> showres = new JList<>(results);
		JScrollPane scroll = new JScrollPane(showres);
		showres.addListSelectionListener(new SimilaritListListener(group, showres, confirmbutton));
		this.add(scroll, BorderLayout.CENTER);
		this.add(confirmbutton, BorderLayout.SOUTH);
		this.confirmbutton.addActionListener(new GoToSimilarGroupListener(window));
		this.setPreferredSize(new Dimension(sizex, sizey));
		this.setVisible(true);
	}

	public int definedSizeY() {
		return sizey;
	}

	public int definedSizeX() {
		return sizex;
	}

}













class SimilaritListListener implements ListSelectionListener {
	JList<String> list;
	Group group;
	JButton confirmbutton; 
	public SimilaritListListener(Group group, JList<String> list, JButton confirmbutton) {
		super();
		this.list = list;
		this.group = group;
		this.confirmbutton = confirmbutton;
	}

	@Override
	public void valueChanged(ListSelectionEvent e) {
		if (!e.getValueIsAdjusting()) {
			String groupname = list.getSelectedValue();
			if(groupname == null) {
				confirmbutton.setText("no group selected");
				return;
			}
			Group othergroup = Group.getGroup(groupname);
			if(othergroup == null) {
				System.out.println("CANT COMPUTE SIMILARITY REPORT");
				return;
			}
			
			double result = group.similarityReport(othergroup);
			System.out.println(result);
			DecimalFormat df = new DecimalFormat("#######.###");
			confirmbutton.setText("<html>Go to " + groupname + " <br>(Affinity Score: " + df.format(result) + ")</html>");
		}
	}
}









class JoinListener implements ActionListener {
	Group group;
	Component generalpanel;

	JButton joinbutton;
	JButton leavebutton;

	public JoinListener(Group group, Component whereToDisplayMessage, JButton joinbutton, JButton leavebutton) {
		this.group = group;
		this.generalpanel = whereToDisplayMessage;
		this.leavebutton = leavebutton;
		this.joinbutton = joinbutton;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		if(Application.currentuser == null) {
			return;
		}
			try {
				group.addCitizen(Application.currentuser);
				joinbutton.setVisible(false);
				leavebutton.setVisible(true);

			} catch (GroupContainsUserException e) {
				JOptionPane.showMessageDialog(generalpanel, "Can't join " + e);
			}
	}

		
	
}

class LeaveListener implements ActionListener {
	Group group;
	Component generalpanel;

	JButton joinbutton;
	JButton leavebutton;

	public LeaveListener(Group group, Component whereToDisplayMessage, JButton joinbutton, JButton leavebutton) {
		this.group = group;
		this.generalpanel = whereToDisplayMessage;
		this.leavebutton = leavebutton;
		this.joinbutton = joinbutton;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		try {
			group.removeCitizen(Application.currentuser);
			leavebutton.setVisible(false);
			joinbutton.setVisible(true);
		} catch (RemoveRepresentativeException | MemberNotContainedException e) {
			JOptionPane.showMessageDialog(generalpanel, "Can't leave " + e);
		}
	}

		
	
}


class TreeButtonListener implements TreeSelectionListener {
	JTree tree;
	Window window;

	public TreeButtonListener(Window window, JTree tree) {
		super();
		this.tree = tree;
		this.window = window;
	}

	@Override
	public void valueChanged(TreeSelectionEvent e) {
		Group group = Group.getGroup(tree.getLastSelectedPathComponent().toString());
		window.showPanel(new GroupScreen(group, window));
	}
}

class ListButtonListener implements ListSelectionListener {
	JList<String> list;
	Window window;
	public ListButtonListener(JList<String> list, Window window) {
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


class GoToSimilarGroupListener implements ActionListener {
	Window window;
	public GoToSimilarGroupListener(Window window) {
		this.window = window;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		if (evt.getActionCommand() == "no group selected") {
			return;
		} else {
			String[] splitter = evt.getActionCommand().split(" ");
			window.showPanel(new GroupScreen(Group.getGroup(splitter[2]), window));
			
		}
	}
}



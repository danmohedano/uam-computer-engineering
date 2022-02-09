/**
 * 
 */
package gui.project;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.border.TitledBorder;

import compositePattern.Group;
import gui.window.ICard;
import gui.window.Window;

/**
 * Main panel for the creation of a project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class ProjectCreation extends JPanel implements ICard{
	private JLabel title = new JLabel("Create A Project", JLabel.CENTER);
	private MainFormulario centralPanel = new MainFormulario();
	private JButton next = new JButton("Next");
	
	private int sizex = 850;
	private int sizey = 600;
	
	public ProjectCreation(Window window) {
		this.setBackground(Color.WHITE);
		
		next.addActionListener(new ConfirmProject(window, this, centralPanel.getNameField(), centralPanel.getDescriptionField(), centralPanel.getAmountField(), centralPanel.getGroupBox(), centralPanel.getType()));
		JPanel jp = new JPanel();
		jp.add(next);
		jp.setPreferredSize(new Dimension(100, 50));
		
		this.setLayout(new BorderLayout());
		title.setFont(new Font(super.getFont().getFontName(), Font.BOLD, 24));
		this.add(title, BorderLayout.NORTH);
		this.add(centralPanel, BorderLayout.CENTER);
		this.add(jp, BorderLayout.SOUTH);
		
		this.setPreferredSize(new Dimension(this.sizex,this.sizey));
	}
	
	public static void main(String[] args) {
		JFrame jf = new JFrame();
		ProjectCreation test = new ProjectCreation(null);
		jf.setTitle("Test");
		jf.setSize(600,400);
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);
		jf.add(test);
	}
	
	public int definedSizeX() {return this.sizex;}
	
	public int definedSizeY() {return this.sizey;}
	
	public JPanel getPanel() {return this;}
}

/**
 * Class to store the main form
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
class MainFormulario extends JPanel{
	private BaseTextFormulario name = new BaseTextFormulario("Name:", "", 20);
	private BaseTextFormulario description = new BaseTextFormulario("Description:", "", 20);
	private BaseTextFormulario amount = new BaseTextFormulario("Amount:", "", 20);
	private GroupBox combo = new GroupBox();
	private JPanel buttons = new JPanel();
	private JRadioButton jrbs[] = {new JRadioButton("Infrastructure"), new JRadioButton("Social Issues")};
	private GridBagConstraints gbc = new GridBagConstraints();
	private ButtonGroup bg = new ButtonGroup();
	
	public MainFormulario() {
		//Setup project type buttons
		this.setBackground(Color.WHITE);
		buttons.setLayout(new GridLayout(0, 1));
		buttons.setBorder(BorderFactory.createTitledBorder(null, "Select the type of the project:", TitledBorder.CENTER, TitledBorder.CENTER, new JLabel().getFont().deriveFont((float)15.0)));
		buttons.setPreferredSize(new Dimension(combo.definedSizeX(), 75));
		buttons.setBackground(Color.WHITE);
		for (JRadioButton b: this.jrbs) {
			bg.add(b);
			buttons.add(b);
			b.setBackground(Color.WHITE);
		}
		
		this.setLayout(new GridBagLayout());
		
		gbc.gridx = 0;
		gbc.gridy = 0;
		this.add(name, gbc);
		gbc.gridx = 0;
		gbc.gridy = 1;
		this.add(description, gbc);
		gbc.gridx = 0;
		gbc.gridy = 2;
		this.add(amount, gbc);
		gbc.gridx = 1;
		gbc.gridy = 0;
		this.add(combo, gbc);
		gbc.gridx = 1;
		gbc.gridy = 1;
		gbc.gridheight = 2;
		gbc.fill = GridBagConstraints.VERTICAL;
		this.add(buttons, gbc);
		this.setPreferredSize(new Dimension(550,450));
	}
	
	public JTextField getNameField() {
		return this.name.getText();
	}
	
	public JTextField getDescriptionField() {
		return this.description.getText();
	}
	
	public JTextField getAmountField() {
		return this.amount.getText();
	}
	
	public JComboBox<String> getGroupBox() {
		return this.combo.getBox();
	}
	
	public JRadioButton[] getType() {
		return this.jrbs;
	}
}

/**
 * Class to define the most basic form with a label and an input
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
class BaseTextFormulario extends JPanel{
	private JLabel label;
	private JTextField text;
	
	public BaseTextFormulario(String label, String text, int n) {
		//Initialize components
		this.setBackground(Color.WHITE);
		this.label = new JLabel(label);
		this.text = new JTextField(text, n);
		
		//Set font of components
		this.label.setFont(this.label.getFont().deriveFont((float) 15.0));
		//this.text.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 15));
		
		//Set layout for the panel
		SpringLayout layout = new SpringLayout();
		this.setLayout(layout);
		
		
		//Label 5 pixels from top and left of the container
		layout.putConstraint(SpringLayout.WEST, this.label, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, this.label, 5, SpringLayout.NORTH, this);
		
		//Text field 5 pixels from bottom of label and 5 left of container
		layout.putConstraint(SpringLayout.WEST, this.text, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, this.text, 5, SpringLayout.SOUTH, this.label);
		
		this.add(this.label);
		this.add(this.text);
		this.setPreferredSize(new Dimension(250,75));
		this.setVisible(true);
	}
	
	public JTextField getText() {
		return this.text;
	}
}

/**
 * Listener to confirm the creation of a project and go on to the next creation screen
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class ConfirmProject implements ActionListener{
	private Window generalPanel;
	private Component window;
	private JTextField name;
	private JTextField description;
	private JTextField amount;
	private JComboBox<String> groupName;
	private JRadioButton buttons[];
	
	
	public ConfirmProject(Window generalPanel, Component window, JTextField name, JTextField description, JTextField amount,
			JComboBox<String> groupName, JRadioButton buttons[]) {
		this.generalPanel = generalPanel;
		this.window = window;
		this.name = name;
		this.description = description;
		this.amount = amount;
		this.groupName = groupName;
		this.buttons = buttons;
	}


	@Override
	public void actionPerformed(ActionEvent e) {
		if (name.getText().compareTo("") == 0 || description.getText().compareTo("") == 0 || amount.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(window, "Fill all required fields");
			return;
		}
		
		if (name.getText().length() > 25) {
			JOptionPane.showMessageDialog(window, "Provided name must be shorter than 25 characters.");
			return;
		}
		
		if (description.getText().length() > 500) {
			JOptionPane.showMessageDialog(window, "Provided description must be shorter than 500 characters.");
			return;
		}
		
		try {
			Double.parseDouble(amount.getText());
		}catch(NumberFormatException x) {
			JOptionPane.showMessageDialog(window, "Provided amount must be a number.");
			return;
		}
		
		if (!buttons[0].isSelected() && !buttons[1].isSelected()) {
			JOptionPane.showMessageDialog(window, "Select a type for the project.");
			return;
		}
		
		String n = name.getText();
		String d = description.getText();
		double b = Double.parseDouble(amount.getText());
		Group g = null;
		if (((String)groupName.getSelectedItem()).compareTo("None") != 0) g = Group.getGroup((String)(groupName.getSelectedItem()));
		ICard x;
		if (buttons[0].isSelected()) x = new InfrastructureCreation(generalPanel, n, d, b, g);
		else x = new SocialIssuesCreation(generalPanel, n, d, b, g);
		
		generalPanel.showPanel(x);
	}
	
}


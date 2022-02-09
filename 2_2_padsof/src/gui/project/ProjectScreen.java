/**
 * 
 */
package gui.project;

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
import java.awt.event.WindowEvent;
import java.io.IOException;

import gui.window.ICard;
import gui.window.Window;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SpringLayout;

import application.Application;
import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import es.uam.eps.sadp.grants.InvalidRequestException;
import exception.projectExceptions.InvalidActionProjectException;
import project.*;

/**
 * Class to display the information regarding a project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class ProjectScreen extends JPanel implements ICard{
	private Project project;
	private int sizex = 600;
	private int sizey = 600;
	
	public ProjectScreen(Window window, Project project) {
		this.setBackground(Color.WHITE);
		this.project = project;
		this.setLayout(new BorderLayout());
		
		JPanel botButtons = new JPanel();
		botButtons.setLayout(new GridBagLayout());
		JButton extraInfo = new JButton("Extra info");
		extraInfo.addActionListener(new ExtraInfoListener(this.project));
		JButton submitToGov = new JButton("Submit to GOV");
		submitToGov.addActionListener(new SubmitListener(this, this.project));
		submitToGov.setVisible(false);
		if (Application.currentuser != null && Application.currentuser.checkCreatedProject(this.project) && this.project.getStatus().compareTo(Status.PASSED_THRESHOLD) == 0) submitToGov.setVisible(true);
		
		GridBagConstraints gbc = new GridBagConstraints();
		
		gbc.gridx = 0;
		gbc.gridy = 0;
		botButtons.add(extraInfo, gbc);
		gbc.gridx = 1;
		gbc.gridy = 0;
		botButtons.add(submitToGov, gbc);
		botButtons.setPreferredSize(new Dimension(800, 50));
		
		
		this.add(new InformationPanel(this.project), BorderLayout.CENTER);
		this.add(new Header(this.project), BorderLayout.NORTH);
		this.add(botButtons, BorderLayout.SOUTH);
		this.setPreferredSize(new Dimension(this.sizex, this.sizey));
		
	}
	
	public static void main(String[] args) throws Exception {
		JFrame jf = new JFrame();
		RegisteredCitizen c2 = new RegisteredCitizen("Malphite", "pwdMalphite", "33333333", false);
		SocialIssuesProject more80spop = new SocialIssuesProject("MakeMore80sPOP", "We are tired of reggaeton we want the 80s back!", 50000, c2, "Music Lovers", false);
		ProjectScreen test = new ProjectScreen(null, more80spop);
		jf.setTitle("Test");
		jf.setSize(test.sizex, test.sizey);
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);
		jf.add(test);
	}
	
	public int definedSizeX() {
		return this.sizex;
	}
	
	public int definedSizeY() {
		return this.sizey;
	}

	@Override
	public JPanel getPanel() {
		return this;
	}
}

/**
 * Main information panel in the project screen
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
class InformationPanel extends JPanel{
	private Project project;
	private JLabel type;
	private JLabel doc;
	private JLabel budget;
	private JLabel dls;
	private JLabel description;
	
	private int sizex = 500;
	private int sizey = 400;
	
	public InformationPanel(Project project) {
		this.setBackground(Color.WHITE);
		this.project = project;
		this.buildLabels();
		
		JPanel leftPanel = new JPanel();
		JPanel rightPanel = new JPanel();
		
		leftPanel.setBackground(Color.WHITE);
		rightPanel.setBackground(Color.WHITE);
		
		//setup left panel
		SpringLayout s = new SpringLayout();
		leftPanel.setLayout(s);
		leftPanel.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1, false));
		
		s.putConstraint(SpringLayout.NORTH, this.type, 5, SpringLayout.NORTH, leftPanel);
		s.putConstraint(SpringLayout.WEST, this.type, 5, SpringLayout.WEST, leftPanel);
		
		s.putConstraint(SpringLayout.NORTH, this.doc, 5, SpringLayout.SOUTH, this.type);
		s.putConstraint(SpringLayout.WEST, this.doc, 5, SpringLayout.WEST, leftPanel);
		
		s.putConstraint(SpringLayout.NORTH, this.budget, 5, SpringLayout.SOUTH, this.doc);
		s.putConstraint(SpringLayout.WEST, this.budget, 5, SpringLayout.WEST, leftPanel);
		
		s.putConstraint(SpringLayout.NORTH, this.dls, 5, SpringLayout.SOUTH, this.budget);
		s.putConstraint(SpringLayout.WEST, this.dls, 5, SpringLayout.WEST, leftPanel);
		
		leftPanel.add(this.type); leftPanel.add(this.doc); leftPanel.add(this.budget); leftPanel.add(this.dls);
		leftPanel.setPreferredSize(new Dimension(this.sizex/2, this.sizey-100));
		//setup right panel
		SpringLayout s2 = new SpringLayout();
		rightPanel.setLayout(s2);
		rightPanel.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1, false));
		s2.putConstraint(SpringLayout.NORTH, this.description, 5, SpringLayout.NORTH, rightPanel);
		s2.putConstraint(SpringLayout.WEST, this.description, 5, SpringLayout.WEST, rightPanel);
		rightPanel.add(this.description);
		rightPanel.setPreferredSize(new Dimension(this.sizex/2, this.sizey-100));
		this.description.setPreferredSize(new Dimension(this.sizex/2, this.sizey-100));
		
		//setup information panel
		SpringLayout mainLayout = new SpringLayout();
		this.setLayout(mainLayout);
		mainLayout.putConstraint(SpringLayout.NORTH, leftPanel, 5, SpringLayout.NORTH, this);
		mainLayout.putConstraint(SpringLayout.WEST, leftPanel, 5, SpringLayout.WEST, this);
		mainLayout.putConstraint(SpringLayout.NORTH, rightPanel, 5, SpringLayout.NORTH, this);
		mainLayout.putConstraint(SpringLayout.WEST, rightPanel, 5, SpringLayout.EAST, leftPanel);
		this.setBorder(BorderFactory.createTitledBorder("<html><b>Information</b></html>"));
		this.add(leftPanel); this.add(rightPanel);
		this.setPreferredSize(new Dimension(this.sizex, this.sizey));
	}
	
	private void buildLabels() {
		if (this.project instanceof InfrastructureProject)
			this.type = new JLabel("<html><b>Type:</b> Infrastructure"+"</html>");
		else 
			this.type = new JLabel("<html><b>Type:</b> Social Issues"+"</html>");
		
		this.doc = new JLabel("<html><b>Creation date:</b> " + this.project.getDoc()+"</html>");
		this.budget = new JLabel("<html><b>Budget requested:</b> " + this.project.getMoney()+"</html>");
		this.dls = new JLabel("<html><b>Last support:</b> " + this.project.getDls()+"</html>");
		this.description = new JLabel("<html><b>Description: </b>" + this.project.getDescription()+"</html>");
		this.description.setVerticalAlignment(JLabel.TOP);
		
		this.type.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 15));
		this.doc.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 15));
		this.budget.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 15));
		this.dls.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 15));
		this.description.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 15));
	}
}

/**
 * Header of the project screen
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
class Header extends JPanel{
	private Project project;
	private JLabel name;
	private JLabel creator;
	private JLabel status;
	private JButton sub;
	private JButton vote = new JButton("Vote");
	private JButton popReportRequest = new JButton("Popularity Report");
	private JLabel popReport = new JLabel("");
	
	private int sizex = 500;
	private int sizey = 100;
	
	public Header(Project project) {
		this.setBackground(Color.WHITE);
		this.project = project;
		this.buildComponents();
		SpringLayout layout = new SpringLayout();
		this.setLayout(layout);
		this.popReportRequest.addActionListener(new PReportRequest(this, this.popReport, this.project));
		this.sub.addActionListener(new SubscribeListener(this, this.project, this.sub));
		this.vote.addActionListener(new VoteListener(this, this.vote, this.popReportRequest, this.project, this.status));

		layout.putConstraint(SpringLayout.NORTH, this.name, 5, SpringLayout.NORTH, this);
		layout.putConstraint(SpringLayout.WEST, this.name, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, this.creator, 5, SpringLayout.SOUTH, this.name);
		layout.putConstraint(SpringLayout.WEST, this.creator, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, this.popReportRequest, 5, SpringLayout.SOUTH, this.creator);
		layout.putConstraint(SpringLayout.WEST, this.popReportRequest, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, this.popReport, 5, SpringLayout.SOUTH, this.creator);
		layout.putConstraint(SpringLayout.WEST, this.popReport, 10, SpringLayout.EAST, this.popReportRequest);
		layout.putConstraint(SpringLayout.NORTH, this.status, 5, SpringLayout.NORTH, this);
		layout.putConstraint(SpringLayout.EAST, this.status, -5, SpringLayout.EAST, this);
		layout.putConstraint(SpringLayout.NORTH, this.vote, 5, SpringLayout.SOUTH, this.status);
		layout.putConstraint(SpringLayout.EAST, this.vote, -5, SpringLayout.EAST, this);
		layout.putConstraint(SpringLayout.NORTH, this.sub, 5, SpringLayout.SOUTH, this.status);
		layout.putConstraint(SpringLayout.EAST, this.sub, -5, SpringLayout.WEST, this.vote);
		
		
		this.add(this.name); this.add(this.creator); this.add(this.popReportRequest); this.add(this.popReport);
		this.add(this.status);this.add(this.sub);this.add(this.vote);
		this.setPreferredSize(new Dimension(this.sizex, this.sizey));
	}
	
	private void buildComponents() {
		this.name = new JLabel(this.project.getName());
		this.name.setFont(new Font(super.getFont().getFontName(), Font.BOLD, 24));
		this.creator = new JLabel("Created by " + this.project.getCreator().getName());
		this.creator.setFont(new Font(super.getFont().getFontName(), Font.ITALIC, 15));
		this.creator.setPreferredSize(new Dimension(this.creator.getPreferredSize().width + 10, this.creator.getPreferredSize().height));
		this.popReport.setFont(new Font(super.getFont().getFontName(), Font.BOLD, 15));
		this.status = new JLabel("<html><b>Status: </b>" + this.project.getStatus().toString()+"</html>");
		this.status.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 20));
		if (Application.currentuser == null) {
			this.sub = new JButton();
			this.sub.setVisible(false);
		}
		else if(Application.currentuser.getProjectsSubscribed().contains(this.project)) this.sub = new JButton("Unsubscribe");
		else this.sub = new JButton("Subscribe");
		if (Application.currentuser == null || (this.project.getStatus() != Status.ONGOING && this.project.getStatus() != Status.PASSED_THRESHOLD)) {
			vote.setVisible(false);
			popReportRequest.setVisible(false);
		}
		else if (this.project.getAllVoters().contains(Application.currentuser)) {
			vote.setVisible(false);
			popReportRequest.setVisible(true);
		}
		else{
			vote.setVisible(true);
			popReportRequest.setVisible(false);
		}
		
		this.vote.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 12));
		this.popReportRequest.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 12));
		this.sub.setFont(new Font(super.getFont().getFontName(), Font.PLAIN, 12));
	}
	
	public int definedSizeX() {return this.sizex;}
	public int definedSizeY() {return this.sizey;}
}


/**
 * Listener to request a popularity report
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class PReportRequest implements ActionListener{
	private Component window;
	private JLabel text;
	private Project project;
	
	public PReportRequest(Component window, JLabel text, Project project) {
		this.window = window;
		this.text = text;
		this.project = project;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		if (this.project.getAllVoters().contains(Application.currentuser)) {
			text.setText(Long.toString(project.popularityReport()));
			text.setVisible(true);
		}
		else {
			JOptionPane.showMessageDialog(window, "Must have voted the project to request a popularity report.");
		}
	}
	
}
/**
 * Listener to subscribe/unsubscribe to a project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class SubscribeListener implements ActionListener{
	private Component window;
	private Project project;
	private JButton button;
	
	public SubscribeListener(Component window, Project project, JButton button) {
		this.window = window;
		this.project = project;
		this.button = button;
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		if (Application.currentuser.getProjectsSubscribed().contains(project))	{
			try {
				project.removeSubscriber(Application.currentuser);
			} catch (InvalidActionProjectException e1) {
				JOptionPane.showMessageDialog(window, "Error encountered.");
				JOptionPane.showMessageDialog(window, e1);

			}
			button.setText("Subscribe");
			JOptionPane.showMessageDialog(window, "Correctly unsubscribed from the project.");
		}
		else {
			try {
				project.addSubscriber(Application.currentuser);
			} catch (InvalidActionProjectException e1) {
				JOptionPane.showMessageDialog(window, "Error encountered.");
				JOptionPane.showMessageDialog(window, e1);

			}
			button.setText("Unsubscribe");
			JOptionPane.showMessageDialog(window, "Correctly subscribed to the project.");
		}
	}
	
}

/**
 * Listener to request a voting of the project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class VoteListener implements ActionListener{
	private Component window;
	private JButton vote;
	private JButton pr;
	private Project project;
	private JLabel status;
	
	public VoteListener(Component window, JButton vote, JButton pr, Project project, JLabel status) {
		this.window = window;
		this.vote = vote;
		this.pr = pr;
		this.project = project;
		this.status = status;
	}


	@Override
	public void actionPerformed(ActionEvent e) {
		new VoteWindow(this.window, this.vote, this.pr, this.project, this.status);
	}
	
}

/**
 * Window to vote a project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
class VoteWindow extends JFrame{
	private Component ogwindow;
	private JButton vote = new JButton("Vote");
	private GroupBox groups = new GroupBox();
	private JButton ogButton1;
	private JButton ogButton2;
	private Project project;
	
	public VoteWindow(Component window, JButton og1, JButton og2, Project project, JLabel status) {
		this.ogwindow = window;
		this.ogButton1 = og1;
		this.ogButton2 = og2;
		this.project = project;
		
		this.setTitle("Vote");
		this.setSize(new Dimension(400, 200));
		this.vote.addActionListener(new VoteWindowListener(this.ogwindow, this.ogButton1, this.ogButton2, this.project, this, this.groups.getBox(), status));
		Container cp = this.getContentPane();
		cp.setLayout(new BorderLayout());
		cp.add(groups, BorderLayout.CENTER);
		cp.add(vote, BorderLayout.SOUTH);
		this.setVisible(true);
	}
	
}

/**
 * Listener to confirm the voting of a project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class VoteWindowListener implements ActionListener{
	private Component window;
	private JButton vote;
	private JButton pr;
	private Project project;
	private JFrame frame;
	private JComboBox<String> box;
	private JLabel status;
	
	public VoteWindowListener(Component window, JButton vote, JButton pr, Project project, JFrame frame, JComboBox<String> box, JLabel status) {
		this.window = window;
		this.vote = vote;
		this.pr = pr;
		this.project = project;
		this.frame = frame;
		this.box = box;
		this.status = status;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String s = (String)box.getSelectedItem();
		System.out.println(s);
		if (s.compareTo("None") == 0) {
			try {
				this.project.vote(Application.currentuser);
			} catch (InvalidActionProjectException e1) {
				JOptionPane.showMessageDialog(window, "Error encountered. " + e1);
				return;
			}
		}
		else
		{
			Group g = Group.getGroup(s);
			try {
				this.project.vote(g);
			} catch (Exception e1) {
				JOptionPane.showMessageDialog(window, "Error encountered. " + e1);
				return;
			}
		}
		
		this.status.setText(("<html><b>Status: </b>" + this.project.getStatus().toString()+"</html>"));
		this.vote.setVisible(false);
		this.pr.setVisible(true);
		JOptionPane.showMessageDialog(window, "Correctly voted the project.");
		frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));
	}
	
}

/**
 * Window for the extra info of the project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
class ExtraInfo extends JFrame{
	
	public ExtraInfo(Project project) {
		Container cp = this.getContentPane();
		SpringLayout layout = new SpringLayout();
		cp.setLayout(layout);
		JLabel type;
		if (project instanceof InfrastructureProject) {
			type = new JLabel("<html><b>Type:</b> Infrastructure</html>");
		}
		else {
			type = new JLabel("<html><b>Type:</b> Social Issues</html>");
		}
		JLabel name = new JLabel("<html><b>Name:</b> " + project.getName() + "</html>");
		JLabel description = new JLabel("<html><b>Description:</b> " + project.getDescription() + "</html>");
		JLabel budget = new JLabel("<html><b>Budget requested:</b> " + Double.toString(project.getMoney()) + "</html>");
		type.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
		name.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
		description.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
		budget.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
		
		layout.putConstraint(SpringLayout.NORTH, type, 5, SpringLayout.NORTH, cp);
		layout.putConstraint(SpringLayout.WEST, type, 5, SpringLayout.WEST, cp);
		layout.putConstraint(SpringLayout.NORTH, name, 5, SpringLayout.SOUTH, type);
		layout.putConstraint(SpringLayout.WEST, name, 5, SpringLayout.WEST, cp);
		layout.putConstraint(SpringLayout.NORTH, description, 5, SpringLayout.SOUTH, name);
		layout.putConstraint(SpringLayout.WEST, description, 5, SpringLayout.WEST, cp);
		layout.putConstraint(SpringLayout.NORTH, budget, 5, SpringLayout.SOUTH, description);
		layout.putConstraint(SpringLayout.WEST, budget, 5, SpringLayout.WEST, cp);
		cp.add(type); cp.add(name); cp.add(description); cp.add(budget);
		
		if (project.getBudgetGranted() != null) {
			JLabel budgetGranted = new JLabel("<html><b>Budget granted to the project: </b>"+Double.toString(project.getBudgetGranted()) +"</html>");
			budgetGranted.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
			layout.putConstraint(SpringLayout.NORTH, budgetGranted, 5, SpringLayout.SOUTH, budget);
			layout.putConstraint(SpringLayout.WEST, budgetGranted, 5, SpringLayout.WEST, cp);
			cp.add(budgetGranted);
		}
		
		if (project instanceof InfrastructureProject) {
			JLabel schemeText = new JLabel("<html><b>Graphical scheme:</b></html>");
			JLabel graphicalScheme = new JLabel(new ImageIcon(((InfrastructureProject) project).getGeneratedFilename()));
			String districts = "<html><b>Districts affected:</b> ";
			if (((InfrastructureProject) project).getDistrictsAffected() != null) {
				for (String x : ((InfrastructureProject) project).getDistrictsAffected()) {
					districts += x + ", ";
				}
			}
			districts += "</html>";
			JLabel districtsAffected = new JLabel(districts);
			layout.putConstraint(SpringLayout.NORTH, schemeText, 5, SpringLayout.SOUTH, budget);
			layout.putConstraint(SpringLayout.WEST, schemeText, 5, SpringLayout.WEST, cp);
			layout.putConstraint(SpringLayout.NORTH, graphicalScheme, 5, SpringLayout.SOUTH, schemeText);
			layout.putConstraint(SpringLayout.WEST, graphicalScheme, 5, SpringLayout.WEST, cp);
			layout.putConstraint(SpringLayout.NORTH, districtsAffected, 5, SpringLayout.SOUTH, graphicalScheme);
			layout.putConstraint(SpringLayout.WEST, districtsAffected, 5, SpringLayout.WEST, cp);
			schemeText.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
			districtsAffected.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
			cp.add(graphicalScheme); cp.add(districtsAffected);cp.add(schemeText);
		}
		else {
			JLabel socialGroup = new JLabel("<html><b>Group affected: </b>"+((SocialIssuesProject)project).getSocialGroup()+"</html>");
			JLabel aim;
			if (((SocialIssuesProject)project).isAim()) aim = new JLabel("<html><b>Aim: </b>International</html>");
			else aim = new JLabel("<html><b>Aim: </b>National</html>");
			layout.putConstraint(SpringLayout.NORTH, socialGroup, 5, SpringLayout.SOUTH, budget);
			layout.putConstraint(SpringLayout.WEST, socialGroup, 5, SpringLayout.WEST, cp);
			layout.putConstraint(SpringLayout.NORTH, aim, 5, SpringLayout.SOUTH, socialGroup);
			layout.putConstraint(SpringLayout.WEST, aim, 5, SpringLayout.WEST, cp);
			socialGroup.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
			aim.setFont(new Font(cp.getFont().getFontName(), Font.PLAIN, 15));
			cp.add(socialGroup); cp.add(aim);
		}
		
		
		
		this.setVisible(true);
		this.setTitle("Extra information");
		this.setSize(new Dimension(500,500));
		cp.setBackground(Color.WHITE);
	}
}

/**
 * Listener to display the extra information
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class ExtraInfoListener implements ActionListener{
	private Project project;
	public ExtraInfoListener(Project project) {this.project = project;}

	@Override
	public void actionPerformed(ActionEvent e) {
		new ExtraInfo(project);
	}
	
}

/**
 * Listener to submit to the external application the project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
class SubmitListener implements ActionListener{
	private Project project;
	private Component window;
	public SubmitListener(Component window, Project project) { this.project = project; this.window = window;}

	@Override
	public void actionPerformed(ActionEvent e) {
		try {
			project.sendProject();
			JOptionPane.showMessageDialog(window, "Project correctly sent to the application");
		} catch (InvalidActionProjectException | IOException | InvalidRequestException e1) {
			JOptionPane.showMessageDialog(window, e1);
		}
	}
	
}
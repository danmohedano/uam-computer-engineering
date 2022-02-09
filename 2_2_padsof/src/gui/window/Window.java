package gui.window;

import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.BorderFactory;
import javax.swing.DefaultListCellRenderer;
import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.SpringLayout;
import javax.swing.SwingConstants;
import javax.swing.UIManager;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import application.Application;
import compositePattern.Group;
import exception.appExceptions.AlreadyLogOutException;
import gui.group.GroupCreation;
import gui.group.GroupScreen;
import gui.group.SearchGroupListener;
import gui.project.ProjectCreation;
import gui.project.ProjectScreen;
import gui.project.SearchProjectListener;
import gui.user.AdminsProfile;
import gui.user.UsersProfile;
import persistence.Persistence;
import project.Project;


/**
 * 
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class Window extends JFrame {
	private JPanel cards = new JPanel();
	private CardLayout layout; 
	private MainMenu menu = null;
	private JButton homeButt = new JButton(new ImageIcon("files/civium60per.png"));
	private ICard actualCard = null;
	private boolean loggedin = false;
	
	/**
	 * @param loggedin the loggedin to set
	 */
	public void setLoggedin(boolean loggedin) {
		this.loggedin = loggedin;
	}

	public Window() {
		super("Civium");
		this.layout = new CardLayout();
		ImageIcon icon = new ImageIcon("files/idol.png");
		this.setIconImage(icon.getImage());

		this.menu = new MainMenu(this);
		homeButt.addActionListener(new HomeListener(this));
		homeButt.setBackground(Color.WHITE);
		Container cp = this.getContentPane(); // Obtener el contenedor del Frame
		cp.setLayout(new BorderLayout()); // Le ponemos un layout de borde

		this.setResizable(false);

		cards.setLayout(this.layout);
		cards.add("menu", menu.getPanel());
		
		this.add(homeButt, BorderLayout.NORTH);
		this.add(cards, BorderLayout.SOUTH);
		this.showPanel(new InitialWindow(this));

		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e) {
			System.out.println("Couldn't set the preferred look and feel");
		}
		this.setVisible(true);
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		
		
		 this.addWindowListener(new WindowAdapter() {
	            @Override
	            public void windowClosing(WindowEvent e){
	                Persistence.saveAll();
	                super.windowClosing(e);
	                System.out.println("EXITING");
	            }
	        });
	}
	
	public void resize(int x, int y) {
		this.getCardsContainer().setPreferredSize(new Dimension(x, y));
		this.setPreferredSize(new Dimension(x, y+75));
		this.setResizable(false);
		
		
	    
		this.validate();
		this.repaint();
		this.pack();
		Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
	    this.setLocation(dim.width/2-x/2, dim.height/2 -y/2);

	}
	
	public void showPanel(ICard newcard) {
		if(this.loggedin == false && (actualCard instanceof InitialWindow)) {
			return;
		}
		if(actualCard != null) {
			this.cards.remove(this.actualCard.getPanel());
		}
		this.actualCard = newcard;
		if(newcard == null) {
			newcard = new MainMenu(this);
		}
		
		this.getCardsContainer().add("actualCard", newcard.getPanel());
		this.layout.show(this.getCardsContainer(), "actualCard");

		this.resize(newcard.definedSizeX(), newcard.definedSizeY());

		
	}
	
	public JPanel getCardsContainer() {
		return this.cards;
	}

}


class HomeListener implements ActionListener {
	Window window;

	public HomeListener(Window window) {
		this.window = window;
	}

	public void actionPerformed(ActionEvent e) {
		window.showPanel(null);
	}
}



@SuppressWarnings("serial")
class MainMenu extends JPanel implements ICard {
	private int sizex = 655;
	private int sizey = 500;
	MainGroupPanel searchgroupanel;
	MainProjectPanel searchprojectpanel;
	JButton currentuser;
	public MainMenu(Window window) {
		SpringLayout layout = new SpringLayout();
		this.setLayout(layout);
		this.setBackground(Color.WHITE);
		searchgroupanel = new MainGroupPanel(window);
		searchprojectpanel = new MainProjectPanel(window);
		if(Application.currentuser == null)	currentuser = new JButton("Admin");
		else 								currentuser = new JButton(Application.currentuser.getName());

		Font f = new Font(super.getFont().getFontName(), Font.BOLD, 15);
		currentuser.setFont(f);
		
		JButton logoutbut = new JButton(new ImageIcon("files/logout.png"));
		logoutbut.addActionListener(new LogOut(this, window));
		logoutbut.setPreferredSize(new Dimension(30, 30));
		currentuser.setPreferredSize(new Dimension(100, 30));	
		currentuser.addActionListener(new LoggedInListener(window));
		
		searchgroupanel.setBorder(BorderFactory.createTitledBorder("<html><b>Groups</b></html>"));
		searchprojectpanel.setBorder(BorderFactory.createTitledBorder("<html><b>Projects</b></html>"));

		
		
		layout.putConstraint(SpringLayout.EAST, currentuser, -5, SpringLayout.EAST, this);
		layout.putConstraint(SpringLayout.NORTH, currentuser, 5, SpringLayout.NORTH, this);
		this.add(currentuser);
		layout.putConstraint(SpringLayout.EAST, logoutbut, -5, SpringLayout.WEST, currentuser);
		layout.putConstraint(SpringLayout.NORTH, logoutbut, 5, SpringLayout.NORTH, this);
		this.add(logoutbut);
		layout.putConstraint(SpringLayout.WEST, searchgroupanel, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, searchgroupanel, 5, SpringLayout.SOUTH, logoutbut);
		this.add(searchgroupanel);
		layout.putConstraint(SpringLayout.WEST, searchprojectpanel, 5, SpringLayout.EAST, searchgroupanel);
		layout.putConstraint(SpringLayout.NORTH, searchprojectpanel, 5, SpringLayout.SOUTH, logoutbut);
		this.add(searchprojectpanel);
		
		sizey = searchgroupanel.definedSizeY() +45;
		
		this.setVisible(true);
	}

	public int definedSizeY() {
		return sizey;
	}

	public int definedSizeX() {
		return sizex;
	}

	@Override
	public JPanel getPanel() {
		return this;
	}

}






@SuppressWarnings("serial")
class MainGroupPanel extends JPanel {
	Window window;
	int sizex = 200;
	int sizey = 410;
	JButton confirmbutton = new JButton("Create Group");
	DefaultListModel<String> results;
	public MainGroupPanel(Window window) {
		this.setBackground(Color.WHITE);
		this.window = window;
		this.setLayout(new BorderLayout());
		this.add(confirmbutton, BorderLayout.SOUTH);
		confirmbutton.addActionListener(new CreateGroupListener(window, this));
		JPanel searchbox = new JPanel();
		searchbox.setBackground(Color.WHITE);

		JTextField field = new JTextField(14);
		JButton clicksearch = new JButton();
		clicksearch.setIcon(new ImageIcon("files/search20.gif"));
		clicksearch.setPreferredSize(new Dimension(20, 20));
		
		searchbox.setLayout(new GridBagLayout());
		GridBagConstraints constraints = new GridBagConstraints();
		constraints.gridx = 0; // El ï¿½rea de texto empieza en la columna cero.
		constraints.gridy = 0; // El ï¿½rea de texto empieza en la fila cero
		constraints.gridwidth = 2; // El ï¿½rea de texto ocupa dos columnas.
		constraints.gridheight = 2; // El ï¿½rea de texto ocupa 2 filas.
		searchbox.add(field, constraints);
		GridBagConstraints constraints2 = new GridBagConstraints();
		constraints2.gridx = 2; // El ï¿½rea de texto empieza en la columna cero.
		constraints2.gridy = 0; // El ï¿½rea de texto empieza en la fila cero
		constraints2.gridwidth = 2; // El ï¿½rea de texto ocupa dos columnas.
		constraints2.gridheight = 2; // El ï¿½rea de texto ocupa 2 filas.
		searchbox.add(clicksearch, constraints2);
		
		this.add(searchbox, BorderLayout.NORTH);
		
		results = new DefaultListModel<String>();
		results.addAll(Group.GroupSearch(""));
		clicksearch.addActionListener(new SearchGroupListener(results,field));

		JList<String> showres = new JList<>(results);
		DefaultListCellRenderer renderer = (DefaultListCellRenderer) showres.getCellRenderer();
		renderer.setHorizontalAlignment(SwingConstants.CENTER);
		JScrollPane scroll = new JScrollPane(showres);
		showres.addListSelectionListener(new SearchGroup(window, showres));
		this.add(scroll, BorderLayout.CENTER);
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


class CreateGroupListener implements ActionListener {
	Window window;
	Component component;
	public CreateGroupListener(Window window, Component component) {
		this.window = window;
		this.component = component;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		if(Application.currentuser == null) {
			JOptionPane.showMessageDialog(component, "Sorry you can't create a group");
			return;
		}
		GroupCreation group = new GroupCreation(window);
		window.showPanel(group);
		
	}

		
	
}



class SearchGroup implements ListSelectionListener {
	JList<String> list;
	Window window;
	
	public SearchGroup(Window window, JList<String> list) {
		this.list = list;
		this.window = window;
	}

	@Override
	public void valueChanged(ListSelectionEvent e) {
		String groupname = list.getSelectedValue();
		if(groupname == null) {
			return;
		}
		Group group = Group.getGroup(groupname);
		if(group == null) {
			return;
		}
		list.clearSelection();
		window.showPanel(new GroupScreen(group, window));


	}
}


class LoggedInListener implements ActionListener {
	Window window;
	public LoggedInListener(Window window) {
		this.window = window;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		if(evt.getActionCommand().equals("Admin")) {
			window.showPanel(new AdminsProfile(window));
		}
		else window.showPanel(new UsersProfile(window));
	}

		
	
}


class LogOut implements ActionListener {

	Window window;
	Component comp;
	
	public LogOut(Component comp, Window window) {
		this.comp = comp;
		this.window = window;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		try {
			Application.logout();
			window.setLoggedin(false);
			window.showPanel(new InitialWindow(window));
						
		} catch (AlreadyLogOutException e1) {
			JOptionPane.showMessageDialog(comp, e1);
		}
		
		
	}
}

@SuppressWarnings("serial")
class MainProjectPanel extends JPanel{
	private Window window;
	private int sizex = 425;
	private int sizey = 410;
	private JButton create = new JButton("Create Project");
	private MainProjectGenericPanel inf;
	private MainProjectGenericPanel soc;
	
	public MainProjectPanel(Window window) {
		this.window = window;
		this.setBackground(Color.WHITE);
		SpringLayout s = new SpringLayout();
		this.setLayout(s);
		create.addActionListener(new CreateProjectListener(this.window, this));
		inf = new MainProjectGenericPanel(window, true);
		soc = new MainProjectGenericPanel(window, false);
		s.putConstraint(SpringLayout.NORTH, inf, 0, SpringLayout.NORTH, this);
		s.putConstraint(SpringLayout.WEST, inf, 5, SpringLayout.WEST, this);
		s.putConstraint(SpringLayout.NORTH, soc, 0, SpringLayout.NORTH, this);
		s.putConstraint(SpringLayout.WEST, soc, 5, SpringLayout.EAST, inf);
		s.putConstraint(SpringLayout.NORTH, create, 2, SpringLayout.SOUTH, inf);
		s.putConstraint(SpringLayout.WEST, create, 5, SpringLayout.WEST, this);
		
		create.setPreferredSize(new Dimension(sizex-20, 20));
		this.add(inf);
		this.add(soc);
		this.add(create);
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

@SuppressWarnings("serial")
class MainProjectGenericPanel extends JPanel {
	Window window;
	int sizex = 200;
	int sizey = 365;
	DefaultListModel<String> results;
	public MainProjectGenericPanel(Window window, boolean type) {
		this.setBackground(Color.WHITE);
		this.window = window;
		this.setLayout(new BorderLayout());
		JPanel searchbox = new JPanel();
		searchbox.setBackground(Color.WHITE);

		JTextField field = new JTextField(14);
		JButton clicksearch = new JButton();
		clicksearch.setIcon(new ImageIcon("files/search20.gif"));
		clicksearch.setPreferredSize(new Dimension(20, 20));
		
		searchbox.setLayout(new GridBagLayout());
		GridBagConstraints constraints = new GridBagConstraints();
		constraints.gridx = 0; // El ï¿½rea de texto empieza en la columna cero.
		constraints.gridy = 0; // El ï¿½rea de texto empieza en la fila cero
		constraints.gridwidth = 2; // El ï¿½rea de texto ocupa dos columnas.
		constraints.gridheight = 2; // El ï¿½rea de texto ocupa 2 filas.
		searchbox.add(field, constraints);
		GridBagConstraints constraints2 = new GridBagConstraints();
		constraints2.gridx = 2; // El ï¿½rea de texto empieza en la columna cero.
		constraints2.gridy = 0; // El ï¿½rea de texto empieza en la fila cero
		constraints2.gridwidth = 2; // El ï¿½rea de texto ocupa dos columnas.
		constraints2.gridheight = 2; // El ï¿½rea de texto ocupa 2 filas.
		searchbox.add(clicksearch, constraints2);
		
		this.add(searchbox, BorderLayout.NORTH);
		
		results = new DefaultListModel<String>();
		results.addAll(Project.projectSearch("", type));
		clicksearch.addActionListener(new SearchProjectListener(results,field, type));

		JList<String> showres = new JList<>(results);
		DefaultListCellRenderer renderer = (DefaultListCellRenderer) showres.getCellRenderer();
		renderer.setHorizontalAlignment(SwingConstants.CENTER);
		JScrollPane scroll = new JScrollPane(showres);
		showres.addListSelectionListener(new SearchProject(window, showres));
		this.add(scroll, BorderLayout.CENTER);
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

class SearchProject implements ListSelectionListener {
	private JList<String> list;
	private Window window;
	
	public SearchProject(Window window, JList<String> list) {
		this.list = list;
		this.window = window;
	}

	@Override
	public void valueChanged(ListSelectionEvent e) {
		String projectname = list.getSelectedValue();
		if(projectname == null) {
			return;
		}
		Project project = Project.getProject(projectname);
		if(project == null) {
			return;
		}
		list.clearSelection();
		window.showPanel(new ProjectScreen(window, project));
	}
}

class CreateProjectListener implements ActionListener {
	private Window window;
	private Component component;
	public CreateProjectListener(Window window, Component component) {
		this.window = window;
		this.component = component;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
		if(Application.currentuser == null) {
			JOptionPane.showMessageDialog(component, "Sorry you can't create a project");
			return;
		}
		ProjectCreation project = new ProjectCreation(window);
		window.showPanel(project);
		
	}	
}



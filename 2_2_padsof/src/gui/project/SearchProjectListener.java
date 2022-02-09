package gui.project;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.DefaultListModel;
import javax.swing.JTextField;

import project.Project;

/**
 * Listener to search for a project
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class SearchProjectListener implements ActionListener {
	private DefaultListModel<String> listaresults;
	private JTextField contains; 
	private boolean type;

	public SearchProjectListener(DefaultListModel<String> listaresults, JTextField contains, boolean type) {
		this.listaresults = listaresults;
		this.contains = contains;
		this.type = type;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
			listaresults.removeAllElements();
			for(String result: Project.projectSearch(contains.getText(), this.type)) {
				listaresults.addElement(result);
			}
			
	}

}

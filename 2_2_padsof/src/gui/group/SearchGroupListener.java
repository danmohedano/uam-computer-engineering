package gui.group;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.DefaultListModel;
import javax.swing.JTextField;

import compositePattern.Group;

public class SearchGroupListener implements ActionListener {
	DefaultListModel<String> listaresults;
	JTextField contains; 

	public SearchGroupListener(DefaultListModel<String> listaresults, JTextField contains) {
		this.listaresults = listaresults;
		this.contains = contains;
	}

	@Override
	public void actionPerformed(ActionEvent evt) {
			listaresults.removeAllElements();
			for(String result: Group.GroupSearch(contains.getText())) {
				listaresults.addElement(result);
			}
			
	}

		
	
}
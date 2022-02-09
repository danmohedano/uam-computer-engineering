package gui.group;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.SortedSet;
import java.util.TreeSet;

import javax.swing.*;

import application.Application;
import compositePattern.Group;
import exception.groupExceptions.GroupAlreadyExistsException;
import gui.window.ICard;
import gui.window.Window;

/**
 * Group creation
 * 
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class GroupCreation extends JPanel implements ICard {

	private FormularioNombre formulario = new FormularioNombre(); // Hereda de JPanel
	private ListaPadres lista = new ListaPadres();
	private JButton ok = new JButton();

	private int sizex = 0;
	private int sizey = 0;

	public int definedSizeX() {
		return this.sizex;
	}

	public int definedSizeY() {
		return this.sizey+40;
	}

	public GroupCreation(Window window) {
		this.setBackground(Color.WHITE);
		formulario.setBackground(Color.WHITE);
		ok.setIcon(new ImageIcon("files/ok30.png"));
		ok.setPreferredSize(new Dimension(40, 40));
		ok.setBackground(Color.WHITE);

		Container cp = this;
		SpringLayout layout = new SpringLayout();
		cp.setLayout(layout);

		JPanel ventana = this;
		this.ok.addActionListener(new ConfirmGroup(ventana, formulario.getTextField(), lista.getLista(), window));

		layout.putConstraint(SpringLayout.WEST, formulario, 5, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, formulario, 5, SpringLayout.NORTH, this);
		
		layout.putConstraint(SpringLayout.WEST, lista, 5, SpringLayout.WEST, formulario);
		layout.putConstraint(SpringLayout.NORTH, lista, 5, SpringLayout.SOUTH, formulario);

		layout.putConstraint(SpringLayout.WEST, ok, 120, SpringLayout.WEST, this);
		layout.putConstraint(SpringLayout.NORTH, ok,5, SpringLayout.SOUTH, lista);

		


		this.add(formulario);
		this.add(ok);
		this.add(lista);

		// this.pack();
		sizex= lista.sizex +35;
		sizey = lista.sizey + formulario.sizey + 30;
		this.setPreferredSize(new Dimension(sizex, sizey));

		this.setVisible(true);
	}

	@Override
	public JPanel getPanel() {
		return this;
	}

}

@SuppressWarnings("serial")
class FormularioNombre extends JPanel {
	private JLabel label;
	private JTextField field;
	int sizey = 25;

	public FormularioNombre() {
		SpringLayout layout = new SpringLayout(); // Layout basado en restricciones...
		this.setLayout(layout); // muy flexible, pero de bajo nivel.
		// Componentes a colocar...
		label = new JLabel("Nombre: ");
		field = new JTextField("", 23);

		// La izquierda (WEST) de label estará a 5 pixels de la izquierda del contenedor
		layout.putConstraint(SpringLayout.WEST, label, 5, SpringLayout.WEST, this);
		// El norte (NORTH) de label estará a 5 pixels del norte del contenedor
		layout.putConstraint(SpringLayout.NORTH, label, 7, SpringLayout.NORTH, this);

		// La izquierda de field estará a 5 pixels desde el borde derecho (EAST) de
		// label
		layout.putConstraint(SpringLayout.WEST, field, 5, SpringLayout.EAST, label);
		// El norte de field estará a 5 pixels desde el norte del contenedor
		layout.putConstraint(SpringLayout.NORTH, field, 5, SpringLayout.NORTH, this);

		this.add(label);
		this.add(field);
		this.setPreferredSize(new Dimension(250, sizey)); // importante: tamaño preferido de este panel
		this.setVisible(true);
	}

	public JTextField getTextField() {
		return field;
	}
}

@SuppressWarnings("serial")
class ListaPadres extends JPanel {
	private JList<String> lista;
	public int sizex = 250;
	public int sizey = 120;
	public ListaPadres() {
		this.setLayout(new BorderLayout());

		SortedSet<String> firstversion = new TreeSet<>();
		for (Group myGroup : Application.currentuser.getGroupsRepresented()) {
			firstversion.add(myGroup.getName());
			if (myGroup.getName().length() > sizex)
				sizex = myGroup.getName().length();
		}
		ArrayList<String> listaui = new ArrayList<String>();
		listaui.addAll(firstversion);
		listaui.add(0, "Root");

		
		String[] argumentui = new String[listaui.size()];
		argumentui = listaui.toArray(argumentui);

		lista = new JList<String>(argumentui);
		JScrollPane jsc = new JScrollPane(lista);

		lista.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		lista.setLayoutOrientation(JList.VERTICAL);
		lista.setVisibleRowCount(5);

		jsc.setPreferredSize(new Dimension(sizex, sizey));
		this.add(jsc);
		this.setPreferredSize(new Dimension(sizex, sizey+5)); // importante: tamaño preferido de este panel

		this.setVisible(true);
	}

	public JList<String> getLista() {
		
		return lista;
	}

}

class ConfirmGroup implements ActionListener {
	private Component ventana;
	private JList<String> listaresult;
	private JTextField formularioresult;
	Window window;

	public ConfirmGroup(Component ventana, JTextField formularioresult, JList<String> listaresult, Window window) {
		super();
		this.ventana = ventana;
		this.listaresult = listaresult;
		this.formularioresult = formularioresult;
		this.window = window;
	}

	public void actionPerformed(ActionEvent e) {

		if (formularioresult.getText().compareTo("") == 0) {
			JOptionPane.showMessageDialog(ventana, "Write a valid name");
			return;
		}
		
		if (listaresult.getSelectedValue() == null || listaresult.getSelectedValue().compareTo("Root") == 0) {
			if (JOptionPane.showConfirmDialog(ventana, "Do you want to create this group?\nName: " + formularioresult.getText(),
					"Confirm creation", JOptionPane.OK_CANCEL_OPTION) == 0) {
				if (window == null) {
					JOptionPane.showMessageDialog(ventana, "No Layout was provided so can't create group");
				}
				Group newgroup;
				try {
					newgroup = new Group(formularioresult.getText(), Application.currentuser);
					window.showPanel(new GroupScreen(newgroup, window));
				} catch (GroupAlreadyExistsException e1) {
					JOptionPane.showMessageDialog(ventana, e1);
				}
			}

			return;
		}

		else {
			if (JOptionPane.showConfirmDialog(ventana,
					"Do you want to create this group?\nName: " + formularioresult.getText() + "\nSon of: " + listaresult.getSelectedValue(),
					"Confirm creation", JOptionPane.OK_CANCEL_OPTION) == 0) {
				if (window == null) 
					JOptionPane.showMessageDialog(ventana, "No Layout was provided so can't create group");
				else {
					Group father = Group.getGroup(listaresult.getSelectedValue());
					if(father == null) {
						JOptionPane.showMessageDialog(ventana, "Sorry the father selected is no longer available");
						return;
					}
					Group newgroup;
					try {
						newgroup = new Group(formularioresult.getText(), Application.currentuser, father);
						window.showPanel(new GroupScreen(newgroup, window));
					} catch (Exception e1) {
						JOptionPane.showMessageDialog(ventana, e1);
					}
				}
				
			}

			return;
		}
	}
}

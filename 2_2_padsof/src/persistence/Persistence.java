package persistence;
import java.io.*;
import java.util.*;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import project.*;


/**
 * Persistance class to store the whole project
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */

public class Persistence {
	public static String fileextension = ".joi";
	public static String filenamegroups = "groups";
	public static String filenameprojects = "projects";
	public static String filenameusers = "users";
	
	
	/**
	 * saves the objects to the file  specified in the class used in conjunction with readAll
	 * @return true if it was a succesfull false otherwise
	 */
	public static boolean saveAll() {
		
		return  saveProjects(filenameprojects + fileextension) &&
				saveGroups (filenamegroups + fileextension) &&
				saveCitizens(filenameusers + fileextension);
	}
	
	/**
	 * reads the objects from the filename specified in the class used in conjunction with saveAll
	 * @return true if it was a succesfull false otherwise
	 */
	public static boolean readAll() {
		SortedSet<Group> allgroups = loadGroups(filenamegroups + fileextension);
		SortedSet<Project> allprojects = loadProjects(filenameprojects+ fileextension);
		SortedSet<RegisteredCitizen> allusers = loadCitizens(filenameusers + fileextension);
        
		if(allgroups == null|| allprojects == null|| allusers == null) {
			return false;
		}
		Project.setAllProjects(allprojects);
		Group.setAllGroups(allgroups);
		RegisteredCitizen.setAllCitizens(allusers);
		
		return true;
	}
	
	/**
	 * saves projects
	 * @param filename of the file to save
	 * @return true if it was succesfull false otherwise
	 */
	private static boolean saveProjects(String filename) {
		try {
			FileOutputStream file = new FileOutputStream(filename); 
			ObjectOutputStream out = new ObjectOutputStream(file); 
			
			out.writeObject(Project.getAllProjects().size());
			for(Project myProj: Project.getAllProjects()) {
				out.writeObject(myProj);
			}
			out.writeObject(Project.getThreshold());


            out.close(); 
            file.close(); 
	        return true;
		}
		catch(IOException ex) { 
            System.out.println("Didn't recover previous  writing projects"); 
            return false;
        }
	}
	/**
	 * saves projects
	 * @param filename of the file to save
	 * @return true if it was succesfull false otherwise
	 */
	private static boolean saveGroups(String filename) {
		try {
			FileOutputStream file = new FileOutputStream(filename); 
			ObjectOutputStream out = new ObjectOutputStream(file); 
			
			out.writeObject(Group.getAllGroups().size());
			for(Group myGroup: Group.getAllGroups()) {
				out.writeObject(myGroup);
			}

            out.close(); 
            file.close(); 
	        return true;
		}
		catch(IOException ex) { 
            System.out.println("Didn't recover previous  writing projects"); 
            return false;
        }
	}
	/**
	 * saves projects
	 * @param filename of the file to save
	 * @return true if it was succesfull false otherwise
	 */
	private static boolean saveCitizens(String filename) {
		try {
			FileOutputStream file = new FileOutputStream(filename); 
			ObjectOutputStream out = new ObjectOutputStream(file); 
			
			out.writeObject(RegisteredCitizen.getAllCitizens().size());
			for(RegisteredCitizen myUser: RegisteredCitizen.getAllCitizens()) {
				out.writeObject(myUser);
			}

            out.close(); 
            file.close(); 
	        return true;
		}
		catch(IOException ex) { 
            System.out.println("Didn't recover previous  writing projects"); 
            return false;
        }
	}

	
	
	/**
	 * saves projects
	 * @param filename of the file to load
	 * @return true if it was succesfull false otherwise
	 */
	private static SortedSet<Project> loadProjects(String filename) {
		FileInputStream file;
		ObjectInputStream in;
		try {
			file = new FileInputStream(filename); 
            in = new ObjectInputStream(file); 
            
            SortedSet<Project> projectsread = new TreeSet<>();
            int size = (int)in.readObject();
            
            for(; size>0; size-=1) {
                Object myProj = in.readObject();
             
                if(myProj instanceof Project == false) {
                	System.out.println("Error: Not readed a Project");
                	in.close(); 
                    file.close(); 
                	return null;
                }
            	projectsread.add((Project)myProj);
            }
            Project.setThreshold((int)in.readObject());
            
            in.close(); 
            file.close(); 
            return (SortedSet<Project>)projectsread;
		}
		
		catch(Exception ex) 
        { 
			
            System.out.println("Didn't recover previous projects"); 

            return null;
        }
		
	}
	/**
	 * saves projects
	 * @param filename of the file to load
	 * @return true if it was succesfull false otherwise
	 */
	private static SortedSet<Group> loadGroups(String filename) {
		FileInputStream file;
		ObjectInputStream in;
		try {
			file = new FileInputStream(filename); 
            in = new ObjectInputStream(file); 
            
            SortedSet<Group> groupsread = new TreeSet<>();
            int size = (int)in.readObject();
            
            for(; size>0; size-=1) {
                Object myGroup = in.readObject();
             
                if(myGroup instanceof Group == false) {
                	System.out.println("Error: Not readed a Group");
                	in.close(); 
                    file.close(); 
                	return null;
                }
            	groupsread.add((Group)myGroup);
            }
            
            in.close(); 
            file.close(); 
            return (SortedSet<Group>)groupsread;
		}
		
		catch(Exception ex) 
        { 
			
            System.out.println("Didn't recover previous groups"); 

            return null;
        }
	}
	/**
	 * saves projects
	 * @param filename of the file to load
	 * @return true if it was succesfull false otherwise
	 */
	private static SortedSet<RegisteredCitizen> loadCitizens(String filename) {
		FileInputStream file;
		ObjectInputStream in;
		try {
			file = new FileInputStream(filename); 
            in = new ObjectInputStream(file); 
            
            SortedSet<RegisteredCitizen> usersread = new TreeSet<>();
            int size = (int)in.readObject();
            
            for(; size>0; size-=1) {
                Object myUser = in.readObject();
             
                if(myUser instanceof RegisteredCitizen == false) {
                	System.out.println("Error: Not readed a Citizen");
                	in.close(); 
                    file.close(); 
                	return null;
                }
            	usersread.add((RegisteredCitizen)myUser);
            }
            
            in.close(); 
            file.close(); 
            return (SortedSet<RegisteredCitizen>)usersread;
		}
		
		catch(Exception ex) 
        { 
			
            System.out.println("Didn't recover previous citizens"); 

            return null;
        }
	}

}


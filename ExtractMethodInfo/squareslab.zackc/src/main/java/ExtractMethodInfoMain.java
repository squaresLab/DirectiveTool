package main.java;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.EnumDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.ObjectCreationExpr;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;


public class ExtractMethodInfoMain {
    public static void main(String args[]){
        //String dirName = "/Users/zack/git/DirectiveTool/temporaryTestOfChange/Application/src/";
        if(args.length != 1 ){
           System.err.println("You must specify the path in the argument");
           System.exit(1);
        }
        String dirName = args[0];
        try {
            Files.walk(Paths.get(dirName))
                    .filter(Files::isRegularFile)
                    .filter(fileName -> fileName.toString().endsWith(".java"))
                    .filter(fileName -> !fileName.toString().endsWith("Test.java"))
                    .forEach(fileName -> parseAndPrintFile(fileName.toString()));

        } catch (IOException ie) {
            System.out.println("there was an io exception that occurred when looking for files in "+dirName);
        }


    }

    public static void parseAndPrintFile(String fileName){
        CompilationUnit cu = null;
        //System.out.println("Starting to parse: "+ fileName);
        try {
            //cu = JavaParser.parse(new File(args[0]));
            cu = JavaParser.parse(new File(fileName));
        } catch (FileNotFoundException fe) {
            //System.err.println("There was a problem reading the file "+args[0]+". Check if the file exists.");
            System.err.println("There was a problem reading the file " + fileName + ". Check if the file exists.");
            System.exit(1);
        } catch (RuntimeException re) {
            System.err.println("There was a problem reading the file " + fileName + ". Check if the file exists.");
            System.exit(1);
        }
        cu.findAll(MethodDeclaration.class).stream()
                .forEach(m -> printMethodInfo(m, fileName));
    }

    public static void printMethodInfo(MethodDeclaration m, String fileName) {
        String methodName = m.getName().toString();
        String methodStartInfo = m.getRange().get().begin.toString();
        String containingClass = "";
        try {
            containingClass = ((ClassOrInterfaceDeclaration) (m.getParentNode().get())).getName().toString();
        } catch (ClassCastException ce){
            try {
                containingClass = ((ObjectCreationExpr) (m.getParentNode().get())).getType().toString();
            } catch (ClassCastException ce2) {
                if (m.getParentNode().get() instanceof EnumDeclaration){
                    return;
                } else {
                    System.err.println(ce2);
                    System.err.println("failed to find the class in the file as the parent node in file " + fileName);
                    System.err.print(m.getParentNode().get().toString());
                    System.exit(1);
                }
            }
        }
        System.out.println(containingClass+", "+ methodName+", "+methodStartInfo+", "+fileName);
        System.out.println("");
    }
}

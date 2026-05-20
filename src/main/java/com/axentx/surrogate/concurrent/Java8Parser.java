package com.axentx.surrogate.concurrent;

import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.DefaultMethodDeclaration;
import org.eclipse.jdt.core.dom.BodyDeclaration;
import org.eclipse.jdt.core.dom.SimpleName;
import org.eclipse.jdt.core.JavaCore;
import java.util.ArrayList;
import java.util.List;

public class Java8Parser {
    public List<DefaultMethodInfo> parseDefaultMethods(String sourceCode) {
        ASTParser parser = ASTParser.newParser(AST.JLS8);
        parser.setSource(sourceCode.toCharArray());
        parser.setResolveBindings(true);
        parser.setKind(ASTParser.K_COMPILATION_UNIT);

        String[] sources = { "" };
        String[] classpaths = { "" };
        parser.setEnvironment(classpaths, sources, null, true);
        parser.setCompilerOptions(JavaCore.getOptions());

        CompilationUnit cu = (CompilationUnit) parser.createAST(null);

        List<DefaultMethodInfo> defaultMethods = new ArrayList<>();

        cu.accept(new ASTVisitor() {
            @Override
            public boolean visit(MethodDeclaration node) {
                if (node.isDefaultMethod()) {
                    DefaultMethodInfo info = new DefaultMethodInfo();
                    info.setMethodName(node.getName().getIdentifier());
                    info.setLineNumber(cu.getLineNumber(node.getStartPosition()));
                    defaultMethods.add(info);
                }
                return super.visit(node);
            }
        });

        return defaultMethods;
    }
}
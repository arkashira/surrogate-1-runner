
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.TypeDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.Set;

public class JavaCodeAnalyzer {

    private static final Set<String> CONCURRENT_COLLECTIONS = new HashSet<>();

    static {
        CONCURRENT_COLLECTIONS.add("java.util.concurrent.CopyOnWriteArrayList");
        CONCURRENT_COLLECTIONS.add("java.util.concurrent.CopyOnWriteArraySet");
        CONCURRENT_COLLECTIONS.add("java.util.concurrent.CopyOnWriteArrayMap");
        // Add more concurrent collections as needed
    }

    public static void analyzeFile(Path filePath) throws IOException {
        String content = Files.readString(filePath);
        CompilationUnit cu = StaticJavaParser.parse(content);

        new VoidVisitorAdapter<Void>() {
            @Override
            public void visit(MethodDeclaration n, Void arg) {
                super.visit(n, arg);
                if (n.isDefault() && n.getBody().isPresent()) {
                    checkSynchronizedBlock(n);
                    checkConcurrentCollectionUsage(n);
                }
            }
        }.visit(cu, null);
    }

    private static void checkSynchronizedBlock(MethodDeclaration method) {
        if (!method.getBody().get().findFirst("synchronized").isPresent()) {
            System.out.printf("Missing synchronized block in default method override: %s.%s()%n",
                    method.getDeclaringClass().get().getNameAsString(),
                    method.getNameAsString());
        }
    }

    private static void checkConcurrentCollectionUsage(MethodDeclaration method) {
        NodeList<Parameter> params = method.getParameters();
        for (Parameter param : params) {
            if (CONCURRENT_COLLECTIONS.contains(param.getType().asString())) {
                System.out.printf("Improper use of non-thread-safe collection in concurrent context: %s.%s(%s)%n",
                        method.getDeclaringClass().get().getNameAsString(),
                        method.getNameAsString(),
                        param.getType().asString());
            }
        }
    }

    public static void main(String[] args) throws IOException {
        Path filePath = Paths.get("/opt/axentx/surrogate-1/src/main/java/com/axentx/surrogate1/JavaCodeAnalyzer.java");
        analyzeFile(filePath);
    }
}
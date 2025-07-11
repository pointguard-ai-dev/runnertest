package com.java.repo.test;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class FetchGitHubRepos {
    private static final String GITHUB_API_BASE = "https://api.github.com";
    private final String personalAccessToken;
    private final String targetDirectory;
    private final ObjectMapper objectMapper;
    
    public FetchGitHubRepos(String personalAccessToken, String targetDirectory) {
        this.personalAccessToken = personalAccessToken;
        this.targetDirectory = targetDirectory;
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Fetches all repositories for the authenticated user
     */
    public List<Repository> fetchAllRepositories() throws Exception {
        List<Repository> repositories = new ArrayList<>();
        int page = 1;
        boolean hasMore = true;
        
        System.out.println("🔍 Fetching repositories from GitHub...");
        
        while (hasMore) {
            String url = GITHUB_API_BASE + "/user/repos?page=" + page + "&per_page=100&sort=updated";
            System.out.println("📄 Fetching page " + page + "...");
            
            String response = makeGitHubApiCall(url);
            JsonNode repos = objectMapper.readTree(response);
            
            if (repos.isArray() && repos.size() > 0) {
                for (JsonNode repo : repos) {
                    Repository repository = new Repository(
                        repo.get("name").asText(),
                        repo.get("clone_url").asText(),
                        repo.get("ssh_url").asText(),
                        repo.get("html_url").asText(),
                        repo.get("private").asBoolean(),
                        repo.get("default_branch").asText(),
                        repo.get("language") != null ? repo.get("language").asText() : "Unknown"
                    );
                    repositories.add(repository);
                }
                page++;
            } else {
                hasMore = false;
            }
        }
        
        System.out.println("✅ Found " + repositories.size() + " repositories");
        return repositories;
    }
    
    /**
     * Fetches repositories for a specific organization
     */
    public List<Repository> fetchOrgRepositories(String orgName) throws Exception {
        List<Repository> repositories = new ArrayList<>();
        int page = 1;
        boolean hasMore = true;
        
        System.out.println("🔍 Fetching repositories for organization: " + orgName);
        
        while (hasMore) {
            String url = GITHUB_API_BASE + "/orgs/" + orgName + "/repos?page=" + page + "&per_page=100";
            System.out.println("📄 Fetching page " + page + "...");
            
            String response = makeGitHubApiCall(url);
            JsonNode repos = objectMapper.readTree(response);
            
            if (repos.isArray() && repos.size() > 0) {
                for (JsonNode repo : repos) {
                    Repository repository = new Repository(
                        repo.get("name").asText(),
                        repo.get("clone_url").asText(),
                        repo.get("ssh_url").asText(),
                        repo.get("html_url").asText(),
                        repo.get("private").asBoolean(),
                        repo.get("default_branch").asText(),
                        repo.get("language") != null ? repo.get("language").asText() : "Unknown"
                    );
                    repositories.add(repository);
                }
                page++;
            } else {
                hasMore = false;
            }
        }
        
        System.out.println("✅ Found " + repositories.size() + " repositories for " + orgName);
        return repositories;
    }
    
    /**
     * Clones all repositories to the target directory
     */
    public void cloneRepositories(List<Repository> repositories) throws Exception {
        // Create target directory if it doesn't exist
        Path targetPath = Paths.get(targetDirectory);
        if (!Files.exists(targetPath)) {
            Files.createDirectories(targetPath);
            System.out.println("📁 Created directory: " + targetDirectory);
        }
        
        System.out.println("🚀 Starting to clone " + repositories.size() + " repositories...");
        
        int successful = 0;
        int failed = 0;
        
        for (int i = 0; i < repositories.size(); i++) {
            Repository repo = repositories.get(i);
            System.out.println("\n[" + (i + 1) + "/" + repositories.size() + "] 📦 Cloning: " + repo.name);
            
            try {
                cloneRepository(repo);
                successful++;
                System.out.println("✅ Successfully cloned: " + repo.name);
            } catch (Exception e) {
                failed++;
                System.err.println("❌ Failed to clone " + repo.name + ": " + e.getMessage());
            }
        }
        
        System.out.println("\n📊 Clone Summary:");
        System.out.println("✅ Successful: " + successful);
        System.out.println("❌ Failed: " + failed);
        System.out.println("📁 All repositories cloned to: " + targetDirectory);
    }
    
    /**
     * Clones a single repository
     */
    private void cloneRepository(Repository repo) throws Exception {
        String repoPath = targetDirectory + File.separator + repo.name;
        
        // Check if repository already exists
        if (Files.exists(Paths.get(repoPath))) {
            System.out.println("⚠️ Repository already exists, pulling latest changes...");
            updateRepository(repoPath);
            return;
        }
        
        // Use clone URL with token for authentication
        String cloneUrl = repo.cloneUrl.replace("https://", "https://" + personalAccessToken + "@");
        
        ProcessBuilder processBuilder = new ProcessBuilder(
            "git", "clone", cloneUrl, repoPath
        );
        
        Process process = processBuilder.start();
        
        // Read output
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("  " + line);
            }
        }
        
        // Read error output
        try (BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()))) {
            String line;
            while ((line = errorReader.readLine()) != null) {
                System.err.println("  " + line);
            }
        }
        
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("Git clone failed with exit code: " + exitCode);
        }
    }
    
    /**
     * Updates an existing repository
     */
    private void updateRepository(String repoPath) throws Exception {
        ProcessBuilder processBuilder = new ProcessBuilder(
            "git", "pull", "origin"
        );
        processBuilder.directory(new File(repoPath));
        
        Process process = processBuilder.start();
        int exitCode = process.waitFor();
        
        if (exitCode == 0) {
            System.out.println("✅ Updated repository");
        } else {
            System.err.println("⚠️ Failed to update repository");
        }
    }
    
    /**
     * Makes an authenticated API call to GitHub
     */
    private String makeGitHubApiCall(String url) throws Exception {
        URL apiUrl = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) apiUrl.openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("Authorization", "Bearer " + personalAccessToken);
        connection.setRequestProperty("Accept", "application/vnd.github.v3+json");
        connection.setRequestProperty("User-Agent", "FetchGitHubRepos/1.0");
        
        int responseCode = connection.getResponseCode();
        if (responseCode != 200) {
            throw new RuntimeException("GitHub API call failed with response code: " + responseCode);
        }
        
        try (Scanner scanner = new Scanner(connection.getInputStream())) {
            StringBuilder response = new StringBuilder();
            while (scanner.hasNextLine()) {
                response.append(scanner.nextLine());
            }
            return response.toString();
        }
    }
    
    /**
     * Repository data class
     */
    public static class Repository {
        public final String name;
        public final String cloneUrl;
        public final String sshUrl;
        public final String htmlUrl;
        public final boolean isPrivate;
        public final String defaultBranch;
        public final String language;
        
        public Repository(String name, String cloneUrl, String sshUrl, String htmlUrl, 
                         boolean isPrivate, String defaultBranch, String language) {
            this.name = name;
            this.cloneUrl = cloneUrl;
            this.sshUrl = sshUrl;
            this.htmlUrl = htmlUrl;
            this.isPrivate = isPrivate;
            this.defaultBranch = defaultBranch;
            this.language = language;
        }
        
        @Override
        public String toString() {
            return String.format("Repository{name='%s', language='%s', private=%s, url='%s'}", 
                               name, language, isPrivate, htmlUrl);
        }
    }
    
    public static void main(String[] args) {
        // Configuration
        // String PAT_TOKEN = System.getenv("GITHUB_PAT_TOKEN");
        String PAT_TOKEN = "ghp_nZF65Y3hw********mWQGD0Bz6kn1GhapG"; // Set this as environment variable
        String TARGET_DIRECTORY = "C:\\Users\\DELL\\Desktop\\Repo-Test"; // Change this to your desired path
        String ORG_NAME = "gpraveen"; // Set this if you want to fetch org repos instead of user repos
        
        try {
            FetchGitHubRepos fetcher = new FetchGitHubRepos(PAT_TOKEN, TARGET_DIRECTORY);
            
            // Fetch repositories
            List<Repository> repositories;
            if (ORG_NAME != null) {
                repositories = fetcher.fetchOrgRepositories(ORG_NAME);
            } else {
                repositories = fetcher.fetchAllRepositories();
            }
            
            // Display repository list
            System.out.println("\n📋 Repository List:");
            for (Repository repo : repositories) {
                System.out.println("  " + repo);
            }
            
            // Ask user for confirmation
            System.out.print("\n❓ Do you want to clone all " + repositories.size() + " repositories? (y/N): ");
            Scanner scanner = new Scanner(System.in);
            String response = scanner.nextLine().trim().toLowerCase();
            
            if (response.equals("y") || response.equals("yes")) {
                // Clone all repositories
                fetcher.cloneRepositories(repositories);
            } else {
                System.out.println("👋 Operation cancelled by user");
            }
            
        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
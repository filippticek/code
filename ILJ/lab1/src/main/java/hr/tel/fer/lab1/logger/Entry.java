package hr.tel.fer.lab1.logger;

public class Entry {
    private String ip;
    private String datetime;
    private String method;
    private String path;
    private String version;
    private String status;
    private String client;

    public Entry(String ip, String datetime, String method, String path, String version, String status, String client) {
        this.ip = ip;
        this.datetime = datetime;
        this.method = method;
        this.path = path;
        this.version = version;
        this.status = status;
        this.client = client;
    }

    public Entry() {

    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getDatetime() {
        return datetime;
    }

    public void setDatetime(String datetime) {
        this.datetime = datetime;
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getClient() { return client; }

    public void setClient(String client) {
        this.client = client;
    }

    @Override
    public String toString() {
        return ip + " " + datetime + " " + method + " " +
                path + " " + version + " " + status + " " + client;
    }
}
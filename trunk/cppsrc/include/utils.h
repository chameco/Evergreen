#ifndef UTILS_H
#define UTILS_H
#define SRAR(cname, name) setResponse(#(name), boost::bind(&cname##::ev_##name, this, _1)); manager->reg(#(name), this)
struct playerspec_event {
	string playername;
	void *data;
};
#endif

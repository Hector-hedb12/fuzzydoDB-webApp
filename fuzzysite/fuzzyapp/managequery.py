class Querym():
  
  def hola(self):
    return "hola"
    
  
  def getq(self, q, att_name, att_type, order_list):
    defq = "SELECT * FROM pokemon";
    if q == None: return defq
    siz = len(q);
    n = len(att_name);
    
    
    if siz < n:
      return defq;
    
    query = [];
    for c in q:
      query.append(ord(c)-ord('a'))
    
    
    a = query[:siz-n]
    b = query[siz-n:siz]
    
    
    
    res = " ORDER BY ";
    
    for i in xrange(len(a)):
      
      index = a[i];
      if index >= att_name: return defq
      
      if att_type[index] == 1:
        m = len(order_list[index])
        if b[index] >= m: return defq
        
        rp = att_name[index] + " STARTING FROM '" + order_list[index][b[index]]+ "'"
      else:
        rp = att_name[index] 
        if b[index] == 0:
          rp = rp + " ASC"
        else:
          rp = rp + " DESC"
      
      if i != len(a)-1:
        rp = rp + ", "
      
      res = res + rp;
    
    return defq + res;


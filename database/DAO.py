from database.DB_connect import DBConnect
from model.artista import Artista
from model.genere import Genere


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getGenere():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        generi = []
        query = """select *
                    from genre"""
        cursor.execute(query, )
        for row in cursor:
            generi.append(Genere(**row))

        cursor.close()
        cnx.close()
        return generi

    @staticmethod
    def getNodes(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        artisti = []
        query = """select distinct ar.*
                    from track t, genre g, album a, artist ar
                    where t.GenreId = g.GenreId and ar.ArtistId = a.ArtistId and a.AlbumId = t.AlbumId and g.Name = %s
                    """
        cursor.execute(query, (genere,))

        for row in cursor:
            artisti.append(Artista(**row))
        cursor.close()
        cnx.close()
        return artisti

    @staticmethod
    def getEdges(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        artisti = []
        query = """
                select t1.Artistid as a1, t2.Artistid as a2
                from(
                select a.ArtistId, i2.CustomerId
                from album a , track t, invoiceline i, invoice i2, genre g
                where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId and t.GenreId = g.GenreId and g.Name = %s
                group by a.ArtistId, i2.CustomerId
                ) as t1, (
                select a.ArtistId, i2.CustomerId
                from album a , track t, invoiceline i, invoice i2, genre g
                where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId and t.GenreId = g.GenreId and g.Name = %s
                group by a.ArtistId, i2.CustomerId
                ) as t2
                where t1.Customerid = t2.Customerid and t1.Artistid < t2.Artistid
                group by t1.Artistid, t2.Artistid"""
        cursor.execute(query, (genere,genere,))

        for row in cursor:
            artisti.append((row["a1"], row["a2"]))
        cursor.close()
        cnx.close()
        return artisti

    @staticmethod
    def getPop(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        artisti = {}
        query = """select a.ArtistId, sum(i.Quantity) as s
                    from album a, track t, invoiceline i, invoice i2, genre g
                    where a.AlbumId = t.AlbumId and i.TrackId = t.TrackId and t.GenreId = g.GenreId and g.Name = %s and i2.InvoiceId = i.InvoiceId 
                    group by a.ArtistId """
        cursor.execute(query, (genere,))

        for row in cursor:
            artisti[(row["ArtistId"])] = row["s"]
        cursor.close()
        cnx.close()
        return artisti

#     @staticmethod
#     def getAllGen():
#         cnx = DBConnect.get_connection()
#         cursor = cnx.cursor(dictionary = True)
#         generi = []
#         query = """select *
#                 from genre"""
#         cursor.execute(query,)
#         for row in cursor:
#             generi.append(Genere(**row))
#
#         cursor.close()
#         cnx.close()
#         return generi
#
#     @staticmethod
#     def getArtisti(genere):
#         cnx = DBConnect.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         artisti = []
#         query = """select a.ArtistId, a.Name
#             from artist a, track t, album al
#             where a.ArtistId = al.ArtistId and t.AlbumId = al.AlbumId and t.GenreId = %s
#             group by a.ArtistId, a.Name"""
#         cursor.execute(query, (genere,))
#
#         for row in cursor:
#             artisti.append(Artista(**row))
#         cursor.close()
#         cnx.close()
#         return artisti
#
#     @staticmethod
#     def edges(mappa, genere):
#         cnx = DBConnect.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         archi = []
#         query = """select a.ArtistId as ArtistId1, a2.ArtistId as ArtistId2
#                 from customer c, invoice i, invoiceline il, customer c2, invoice i2, invoiceline il2, track t, track t2, album a, album a2
#                 where c.CustomerId = i.CustomerId and i.InvoiceId = il.InvoiceId and il.TrackId = t.trackId and t.AlbumId = a.AlbumId and
#                 c2.CustomerId = i2.CustomerId and i2.InvoiceId = il2.InvoiceId and il2.TrackId = t2.trackId and t2.AlbumId = a2.AlbumId and a.ArtistId <> a2.ArtistId and c.CustomerId = c2.CustomerId
#                 AND a.ArtistId < a2.ArtistId and t.GenreId = %s AND t2.GenreId = %s
#                 group by a.ArtistId, a2.ArtistId"""
#         cursor.execute(query, (genere.GenreId, genere.GenreId,))
#
#         for row in cursor:
#             if row["ArtistId1"] in mappa and row["ArtistId2"] in mappa: #IMPORTANTE
#                 archi.append((mappa[row["ArtistId1"]], mappa[row["ArtistId2"]]))
#         cursor.close()
#         cnx.close()
#         return archi
#
#
#     @staticmethod
#     def getAllP(mappa, genere):
#         cnx = DBConnect.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         try:
#             query = """select a.ArtistId, sum(il.quantity) as q
#                         from invoiceline il, track t, album a, genre g
#                         where il.TrackId = t.trackId and t.AlbumId = a.AlbumId
#                         and g.GenreId = t.GenreId
#                         and g.Name  = %s
#                         group by a.ArtistId"""
#             cursor.execute(query, (genere.Name,))
#             result = {}
#             for row in cursor:
#                 if row["ArtistId"] in mappa:
#                     result[row["ArtistId"]] = row["q"]
#             return result
#         finally:
#             cursor.close()
#             cnx.close()
#
#
#         query = """select a.ArtistId, sum(il.quantity) as q
#                 from invoiceline il, track t, album a
#                 where il.TrackId = t.trackId and t.AlbumId = a.AlbumId and a.ArtistId = %s
#                 group by a.ArtistId"""
#         #cursor.execute(query, (artista.ArtistId,))
#         #val = cursor.fetchone()
#         #cursor.close()
#         #cnx.close()
#         #return val["q"]
#
#     @staticmethod
#     def getArchi(genere):
#         cnx = DBConnect.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         archi = []
#         query = """select t1.ArtistId as a1, t2.ArtistId as a2, p1.pop as p1, p2.pop as p2, (p1.pop + p2.pop) as peso
#                     from
#                     (select a.ArtistId, i2.CustomerId, sum(i.Quantity) as pop
#                     from album a, track t, invoiceline i, invoice i2, genre g
#                     where a.AlbumId = t.AlbumId and t.GenreId = %s and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId
#                     group by a.ArtistId, i2.CustomerId) as t1,
#                     (select a.ArtistId, i2.CustomerId, sum(i.Quantity) as pop
#                     from album a, track t, invoiceline i, invoice i2
#                     where a.AlbumId = t.AlbumId and t.GenreId = %s and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId
#                     group by a.ArtistId, i2.CustomerId) as t2,
#                     (SELECT a.ArtistId, SUM(i.Quantity) AS pop
# 				     FROM album a, track t, invoiceline i
# 				     WHERE a.AlbumId = t.AlbumId AND t.GenreId = %s
# 				     AND t.TrackId = i.TrackId
# 				     GROUP BY a.ArtistId) AS p1,
# 				     (SELECT a.ArtistId, SUM(i.Quantity) AS pop
# 				     FROM album a, track t, invoiceline i
# 				     WHERE a.AlbumId = t.AlbumId AND t.GenreId = %s
# 				     AND t.TrackId = i.TrackId
# 				     GROUP BY a.ArtistId) AS p2
#                     where t1.CustomerId = t2.CustomerId and t1.ArtistId < t2.ArtistId
# 					AND t1.ArtistId = p1.ArtistId
# 					AND t2.ArtistId = p2.ArtistId
# 					GROUP BY t1.ArtistId, t2.ArtistId"""
#         cursor.execute(query, (genere, genere, genere, genere))
#         for row in cursor:
#             archi.append((row["a1"], row["a2"], row["p1"], row["p2"], row["peso"]))
#
#         cursor.close()
#         cnx.close()
#         return archi
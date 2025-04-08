from linkedin_api import Linkedin
from fastmcp import FastMCP
import os
import logging

mcp = FastMCP("mcp-linkedin")
logger = logging.getLogger(__name__)

def get_client():
    return Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"), debug=True)

@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieve LinkedIn feed posts.

    :return: List of feed post details
    """
    client = get_client()
    try:
        post_urns = client.get_feed_posts(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"
    
    posts = ""
    for urn in post_urns:
        posts += f"Post by {urn["author_name"]}: {urn["content"]}\n"

    return posts

@mcp.tool()
def search_jobs(keywords: str, limit: int = 3, offset: int = 0, location: str = '') -> str:
    """
    Search for jobs on LinkedIn.
    
    :param keywords: Job search keywords
    :param limit: Maximum number of job results
    :param location: Optional location filter
    :return: List of job details
    """
    client = get_client()
    jobs = client.search_jobs(
        keywords=keywords,
        location_name=location,
        limit=limit,
        offset=offset,
    )
    job_results = ""
    for job in jobs:
        job_id = job["entityUrn"].split(":")[-1]
        job_data = client.get_job(job_id=job_id)

        job_title = job_data["title"]
        company_name = job_data["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["name"]
        job_description = job_data["description"]["text"]
        job_location = job_data["formattedLocation"]

        job_results += f"Job by {job_title} at {company_name} in {job_location}: {job_description}\n\n"

    return job_results

@mcp.tool()
def create_share_update(comment: str, visibility_code: str = 'anyone') -> str:
    """
    Crear una actualización/post en LinkedIn.
    
    :param comment: El contenido del post
    :param visibility_code: Código de visibilidad ('anyone', 'connections-only', 'public')
    :return: Estado de la publicación
    """
    client = get_client()
    try:
        post = client.post(comment, visibility=visibility_code)
        return f"Post creado exitosamente: {post}"
    except Exception as e:
        logger.error(f"Error al crear el post: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_profile(public_id: str = None) -> str:
    """
    Obtener información del perfil de LinkedIn.
    
    :param public_id: ID público del perfil (opcional, si no se proporciona usa el perfil actual)
    :return: Detalles del perfil
    """
    client = get_client()
    try:
        if public_id:
            profile = client.get_profile(public_id)
        else:
            profile = client.get_profile()
        
        return f"""
        Nombre: {profile.get('firstName', '')} {profile.get('lastName', '')}
        Título: {profile.get('headline', '')}
        Ubicación: {profile.get('locationName', '')}
        Industria: {profile.get('industryName', '')}
        """
    except Exception as e:
        logger.error(f"Error al obtener el perfil: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_company(company_id: str) -> str:
    """
    Obtener información de una empresa en LinkedIn.
    
    :param company_id: ID de la empresa en LinkedIn
    :return: Detalles de la empresa
    """
    client = get_client()
    try:
        company = client.get_company(company_id)
        return f"""
        Nombre: {company.get('name', '')}
        Industria: {company.get('industryName', '')}
        Sitio Web: {company.get('companyPageUrl', '')}
        Tamaño: {company.get('staffCountRange', {}).get('start', '')} - {company.get('staffCountRange', {}).get('end', '')} empleados
        Descripción: {company.get('description', '')}
        """
    except Exception as e:
        logger.error(f"Error al obtener información de la empresa: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_connections(limit: int = 10) -> str:
    """
    Obtener lista de conexiones.
    
    :param limit: Número máximo de conexiones a retornar
    :return: Lista de conexiones
    """
    client = get_client()
    try:
        connections = client.get_connections(limit=limit)
        result = "Conexiones:\n"
        for connection in connections:
            result += f"- {connection.get('firstName', '')} {connection.get('lastName', '')}: {connection.get('headline', '')}\n"
        return result
    except Exception as e:
        logger.error(f"Error al obtener conexiones: {e}")
        return f"Error: {e}"

@mcp.tool()
def join_group(group_id: str) -> str:
    """
    Unirse a un grupo de LinkedIn.
    
    :param group_id: ID del grupo
    :return: Estado de la operación
    """
    client = get_client()
    try:
        result = client.join_group(group_id)
        return f"Unido al grupo exitosamente: {result}"
    except Exception as e:
        logger.error(f"Error al unirse al grupo: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_group_posts(group_id: str, limit: int = 10) -> str:
    """
    Obtener posts de un grupo.
    
    :param group_id: ID del grupo
    :param limit: Número máximo de posts a retornar
    :return: Lista de posts del grupo
    """
    client = get_client()
    try:
        posts = client.get_group_posts(group_id, limit=limit)
        result = f"Posts del grupo {group_id}:\n"
        for post in posts:
            result += f"- {post.get('author', '')}: {post.get('content', '')}\n"
        return result
    except Exception as e:
        logger.error(f"Error al obtener posts del grupo: {e}")
        return f"Error: {e}"

@mcp.tool()
def send_invitation(public_id: str, message: str = None) -> str:
    """
    Enviar invitación de conexión.
    
    :param public_id: ID público del perfil a invitar
    :param message: Mensaje opcional para la invitación
    :return: Estado de la invitación
    """
    client = get_client()
    try:
        result = client.send_invitation(public_id, message=message)
        return f"Invitación enviada exitosamente: {result}"
    except Exception as e:
        logger.error(f"Error al enviar invitación: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_pending_invitations(limit: int = 10) -> str:
    """
    Obtener invitaciones pendientes.
    
    :param limit: Número máximo de invitaciones a retornar
    :return: Lista de invitaciones pendientes
    """
    client = get_client()
    try:
        invitations = client.get_invitations(limit=limit)
        result = "Invitaciones pendientes:\n"
        for inv in invitations:
            result += f"- De: {inv.get('fromMember', {}).get('firstName', '')} {inv.get('fromMember', {}).get('lastName', '')}\n"
        return result
    except Exception as e:
        logger.error(f"Error al obtener invitaciones pendientes: {e}")
        return f"Error: {e}"

@mcp.tool()
def send_message(recipients: list, message: str) -> str:
    """
    Enviar mensaje directo.
    
    :param recipients: Lista de IDs de destinatarios
    :param message: Contenido del mensaje
    :return: Estado del envío
    """
    client = get_client()
    try:
        result = client.send_message(recipients=recipients, message=message)
        return f"Mensaje enviado exitosamente: {result}"
    except Exception as e:
        logger.error(f"Error al enviar mensaje: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_conversations(limit: int = 10) -> str:
    """
    Obtener conversaciones recientes.
    
    :param limit: Número máximo de conversaciones a retornar
    :return: Lista de conversaciones
    """
    client = get_client()
    try:
        conversations = client.get_conversations(limit=limit)
        result = "Conversaciones recientes:\n"
        for conv in conversations:
            result += f"- Con: {conv.get('participants', [])[0].get('firstName', '')} {conv.get('participants', [])[0].get('lastName', '')}\n"
        return result
    except Exception as e:
        logger.error(f"Error al obtener conversaciones: {e}")
        return f"Error: {e}"

@mcp.tool()
def manage_company_page(company_id: str, action: str, data: dict = None) -> str:
    """
    Gestionar página de empresa.
    
    :param company_id: ID de la empresa
    :param action: Acción a realizar ('update', 'post', 'get_analytics')
    :param data: Datos adicionales según la acción
    :return: Resultado de la operación
    """
    client = get_client()
    try:
        if action == 'update':
            result = client.update_company_page(company_id, data)
        elif action == 'post':
            result = client.company_share(company_id, data.get('content', ''))
        elif action == 'get_analytics':
            result = client.get_company_analytics(company_id)
        else:
            return "Acción no válida"
        
        return f"Operación completada exitosamente: {result}"
    except Exception as e:
        logger.error(f"Error en la operación de página de empresa: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_post_analytics(post_id: str) -> str:
    """
    Obtener estadísticas de una publicación.
    
    :param post_id: ID de la publicación
    :return: Estadísticas de la publicación
    """
    client = get_client()
    try:
        stats = client.get_post_stats(post_id)
        return f"""
        Estadísticas del post {post_id}:
        Likes: {stats.get('numLikes', 0)}
        Comentarios: {stats.get('numComments', 0)}
        Compartidos: {stats.get('numShares', 0)}
        Impresiones: {stats.get('impressionCount', 0)}
        Engagement: {stats.get('engagementRate', '0%')}
        """
    except Exception as e:
        logger.error(f"Error al obtener estadísticas del post: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    print(search_jobs(keywords="data engineer", location="Jakarta", limit=2))